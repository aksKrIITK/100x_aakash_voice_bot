import asyncio
from typing import List, Dict
import openai
from app.config import settings
from app.providers.llm.base import LLMProvider
from app.services.semantic_rag import semantic_rag_service
from app.personality.question_classifier import classify_question_intent
from app.personality.golden_answers import GOLDEN_ANSWERS
from app.core.logging import logger


class GroqProvider(LLMProvider):
    """Dedicated Groq AI Engine powering Llama 3.3 70B with multi-turn chat recall and semantic RAG fallback."""

    def __init__(self, api_key: str = "", model: str = ""):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.primary_model = model or settings.GROQ_LLM_MODEL or "llama-3.3-70b-versatile"
        self.candidate_models = [
            self.primary_model,
            "llama-3.1-8b-instant",
            "llama3-70b-8192"
        ]
        self.client = None

        if self.api_key:
            try:
                # Groq uses OpenAI-compatible client with base_url="https://api.groq.com/openai/v1"
                self.client = openai.AsyncOpenAI(
                    api_key=self.api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                logger.info(f"Initialized Groq AI Client with model {self.primary_model}")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}")

    async def generate(self, messages: List[Dict[str, str]], system_prompt: str = "") -> str:
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})

        # Inject recalled multi-turn chat history
        for m in messages:
            formatted_messages.append({
                "role": m["role"],
                "content": m["content"]
            })

        # 1. If Groq Client is initialized, attempt live Llama generation with multi-model failover
        if self.client:
            for model_name in self.candidate_models:
                try:
                    response = await self.client.chat.completions.create(
                        model=model_name,
                        messages=formatted_messages,
                        temperature=0.68,
                        max_tokens=400
                    )
                    answer = response.choices[0].message.content.strip()
                    if answer:
                        return answer
                except Exception as e:
                    logger.warning(f"Groq generation with {model_name} failed ({e}). Trying next tier...")

        # 2. Extract last user message for semantic RAG fallback
        last_user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "").strip()
                break

        # Check intent classifier
        intent = classify_question_intent(last_user_msg)
        if intent and intent in GOLDEN_ANSWERS:
            return GOLDEN_ANSWERS[intent]

        # Semantic RAG retrieval over 25+ fine-grained knowledge nodes
        return semantic_rag_service.synthesize_fallback_response(last_user_msg)

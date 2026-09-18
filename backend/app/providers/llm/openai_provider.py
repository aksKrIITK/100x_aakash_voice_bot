import asyncio
import re
from typing import List, Dict
from app.config import settings
from app.providers.llm.base import LLMProvider
from app.personality.question_classifier import classify_question_intent
from app.personality.golden_answers import GOLDEN_ANSWERS
from app.services.semantic_rag import semantic_rag_service
from app.core.logging import logger


class MockLLMProvider(LLMProvider):
    """High-fidelity local personality emulator using Semantic RAG retrieval over Aakash's resume."""

    async def generate(self, messages: List[Dict[str, str]], system_prompt: str = "") -> str:
        await asyncio.sleep(0.1)
        
        last_user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "").strip()
                break

        if not last_user_msg:
            return "Hey there! I'm Aakash's AI voice assistant. Feel free to ask me anything about my journey at IIT Kanpur and JNU, leading backend at WorldRef, founding Godizy, or my agentic AI projects."

        # 1. Direct intent classifier match
        intent = classify_question_intent(last_user_msg)
        if intent and intent in GOLDEN_ANSWERS:
            return GOLDEN_ANSWERS[intent]

        # 2. Greetings
        if re.search(r'\b(hi|hello|hey|greetings|morning|evening|namaste)\b', last_user_msg.lower()):
            return "Hey there! I'm Aakash's AI voice assistant. Feel free to ask me about my engineering journey at IIT Kanpur and JNU, leading backend at WorldRef, founding Godizy, or my agentic AI projects."

        # 3. Semantic RAG Retrieval (indexes 17+ granular resume chunks)
        top_results = semantic_rag_service.retrieve(last_user_msg, top_k=1)
        if top_results and top_results[0][1] >= 1.5:
            top_chunk, score = top_results[0]
            logger.info(f"MockLLMProvider Semantic RAG match: '{top_chunk['topic']}' (score: {score:.2f})")
            return top_chunk["content"]

        # 4. Context-aware conversational fallback
        return (
            f"Regarding {last_user_msg}... from an engineering standpoint, my approach is always to ground decisions in first principles: "
            "analyzing the trade-offs, keeping the architecture modular, and focusing on what delivers the highest real-world reliability."
        )


class OpenAIProvider(LLMProvider):
    """Self-healing LLM provider with multi-model failover (Llama 3.3 70B -> Llama 3.1 8B -> Semantic RAG Engine)."""

    def __init__(self, api_key: str = "", model: str = ""):
        self.fallback = MockLLMProvider()
        self.client = None
        
        self.candidate_models = [
            model or settings.GROQ_LLM_MODEL or "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-70b-8192"
        ]

        groq_key = settings.GROQ_API_KEY or (api_key if settings.LLM_PROVIDER == "groq" else "")
        openai_key = api_key or settings.OPENAI_API_KEY

        if groq_key:
            self.api_key = groq_key
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
                logger.info(f"Initialized Groq LLM Client with primary model {self.candidate_models[0]}")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq Client: {e}. Will use fallback provider.")
        elif openai_key:
            self.api_key = openai_key
            self.candidate_models = [model or settings.OPENAI_MODEL or "gpt-4o-mini"]
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key)
                logger.info(f"Initialized OpenAI LLM Client with model {self.candidate_models[0]}")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI AsyncClient: {e}. Will use fallback provider.")

    async def generate(self, messages: List[Dict[str, str]], system_prompt: str = "") -> str:
        if not self.client:
            return await self.fallback.generate(messages, system_prompt)

        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
            
        for m in messages:
            formatted_messages.append({"role": m["role"], "content": m["content"]})

        # Try models in failover sequence
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
                logger.warning(f"LLM call to model {model_name} failed ({e}). Trying next tier...")

        logger.warning("All external LLM model tiers exhausted. Falling back to semantic RAG provider.")
        return await self.fallback.generate(messages, system_prompt)

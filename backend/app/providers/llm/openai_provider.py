import asyncio
from typing import List, Dict
from app.config import settings
from app.providers.llm.base import LLMProvider
from app.personality.question_classifier import classify_question_intent
from app.personality.golden_answers import GOLDEN_ANSWERS
from app.personality.profile import AAKASH_PROFILE
from app.core.logging import logger


class MockLLMProvider(LLMProvider):
    """High-quality local LLM emulator generating authentic responses when no API key is provided."""
    async def generate(self, messages: List[Dict[str, str]], system_prompt: str = "") -> str:
        await asyncio.sleep(0.3)  # Realistic typing delay
        
        last_user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "")
                break

        intent = classify_question_intent(last_user_msg)
        if intent and intent in GOLDEN_ANSWERS:
            return GOLDEN_ANSWERS[intent]

        msg_lower = last_user_msg.lower()
        if "hello" in msg_lower or "hi" in msg_lower or "hey" in msg_lower:
            return "Hi there! I'm Aakash's AI voice assistant. Ask me anything about my journey, superpower, top growth areas, or work style!"

        if "tech" in msg_lower or "stack" in msg_lower or "skill" in msg_lower:
            return "I work primarily across backend engineering with FastAPI and Spring Boot, React with TypeScript on the frontend, PostgreSQL, and agentic AI frameworks like LangGraph and LangChain."

        if "project" in msg_lower or "built" in msg_lower or "work" in msg_lower:
            return "I enjoy building end-to-end full-stack applications and AI voice agents—focusing on clean architecture, low latency, persistent state management, and simple user interfaces."

        return (
            f"I haven't really thought about '{last_user_msg}' in a structured way yet, "
            "but my instinct is to approach it by breaking down the underlying problem, analyzing trade-offs, and keeping the design simple and reliable."
        )


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str = "", model: str = ""):
        self.fallback = MockLLMProvider()
        self.client = None
        
        # Check Groq API key first, then OpenAI API key
        groq_key = settings.GROQ_API_KEY or (api_key if settings.LLM_PROVIDER == "groq" else "")
        openai_key = api_key or settings.OPENAI_API_KEY

        if groq_key:
            self.api_key = groq_key
            self.model = model or settings.GROQ_LLM_MODEL or "llama-3.3-70b-versatile"
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
                logger.info(f"Initialized Groq LLM Client with model {self.model}")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq Client: {e}. Will try fallback provider.")
        elif openai_key:
            self.api_key = openai_key
            self.model = model or settings.OPENAI_MODEL or "gpt-4o-mini"
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key)
                logger.info(f"Initialized OpenAI LLM Client with model {self.model}")
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

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=400
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"LLM API call failed ({e}). Falling back to local personality provider.")
            return await self.fallback.generate(messages, system_prompt)

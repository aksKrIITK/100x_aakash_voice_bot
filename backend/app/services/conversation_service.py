import time
from typing import Dict, Any, Optional
from app.repositories.conversation_repository import ConversationRepository
from app.personality.question_classifier import classify_question_intent
from app.personality.golden_answers import GOLDEN_ANSWERS
from app.personality.system_prompt import build_system_prompt_with_context
from app.services.llm_service import LLMService
from app.core.logging import logger


class ConversationService:
    def __init__(self, repository: ConversationRepository, llm_service: Optional[LLMService] = None):
        self.repository = repository
        self.llm_service = llm_service or LLMService()

    async def process_chat(self, conversation_id: str, message_text: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Ensure conversation exists and record user message
        await self.repository.ensure_conversation(conversation_id)
        await self.repository.add_message(conversation_id, "user", message_text)

        # 2. Retrieve history (limit to last 6 messages to preserve context while keeping token usage low)
        history = await self.repository.get_messages(conversation_id, limit=6)
        formatted_history = [
            {"role": m["role"], "content": m["content"]}
            for m in history
        ]

        # 3. Classify intent and get golden grounding if applicable
        intent = classify_question_intent(message_text)
        golden_context = GOLDEN_ANSWERS.get(intent, "") if intent else ""

        # 4. Construct prompt and generate answer
        system_prompt = build_system_prompt_with_context(golden_context)
        llm_start = time.time()
        raw_answer = await self.llm_service.generate_response(formatted_history, system_prompt)
        llm_latency = time.time() - llm_start

        # 5. Sanitize and validate answer format
        answer = self._validate_answer(raw_answer, golden_context)

        # 6. Save assistant message
        await self.repository.add_message(conversation_id, "assistant", answer)

        total_time = time.time() - start_time
        logger.info(
            f"Processed chat for conversation {conversation_id} in {total_time:.3f}s (LLM latency: {llm_latency:.3f}s)",
            extra={
                "conversation_id": conversation_id,
                "processing_time": total_time,
                "llm_latency": llm_latency
            }
        )

        return {
            "conversation_id": conversation_id,
            "answer": answer
        }

    def _validate_answer(self, raw_answer: str, golden_context: str) -> str:
        """Sanitizes output to prevent AI disclosure clichés."""
        forbidden_phrases = [
            "As an AI", "As an AI language model", "Based on the provided information",
            "According to the profile", "Aakash would say", "I am an AI"
        ]
        cleaned = raw_answer
        for phrase in forbidden_phrases:
            if phrase in cleaned:
                cleaned = cleaned.replace(phrase, "")
        
        cleaned = cleaned.strip()
        if not cleaned:
            return golden_context if golden_context else "I'm always working to improve my approach to technical problems."
        return cleaned

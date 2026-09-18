import time
from typing import Dict, Any, Optional
from app.repositories.conversation_repository import ConversationRepository
from app.services.agent_workflow import AgenticPersonaPipeline
from app.services.llm_service import LLMService
from app.core.logging import logger


class ConversationService:
    def __init__(self, repository: ConversationRepository, llm_service: Optional[LLMService] = None):
        self.repository = repository
        self.pipeline = AgenticPersonaPipeline(llm_service=llm_service or LLMService())

    async def process_chat(self, conversation_id: str, message_text: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Ensure conversation exists and record user message
        await self.repository.ensure_conversation(conversation_id)
        await self.repository.add_message(conversation_id, "user", message_text)

        # 2. Retrieve history (last 8 messages to preserve multi-turn context across follow-ups)
        history = await self.repository.get_messages(conversation_id, limit=8)
        formatted_history = [
            {"role": m["role"], "content": m["content"]}
            for m in history
        ]

        # 3. Execute multi-stage Agentic Pipeline (Context Resolution -> Semantic RAG -> Persona Synthesis)
        pipeline_result = await self.pipeline.execute(
            user_message=message_text,
            history=formatted_history
        )
        raw_answer = pipeline_result["answer"]
        grounding_context = pipeline_result["grounding_context"]

        # 4. Sanitize and validate answer format
        answer = self._validate_answer(raw_answer, grounding_context)

        # 5. Save assistant message
        await self.repository.add_message(conversation_id, "assistant", answer)

        total_time = time.time() - start_time
        logger.info(
            f"Processed chat for conversation {conversation_id} in {total_time:.3f}s (Top topic: {pipeline_result.get('top_topic')})",
            extra={
                "conversation_id": conversation_id,
                "processing_time": total_time,
                "top_topic": pipeline_result.get("top_topic")
            }
        )

        return {
            "conversation_id": conversation_id,
            "answer": answer
        }

    def _validate_answer(self, raw_answer: str, grounding_context: str) -> str:
        """Sanitizes output to prevent AI disclosure clichés."""
        forbidden_phrases = [
            "As an AI", "As an AI language model", "Based on the provided information",
            "According to the profile", "Aakash would say", "I am an AI",
            "As an AI representation"
        ]
        cleaned = raw_answer
        for phrase in forbidden_phrases:
            if phrase in cleaned:
                cleaned = cleaned.replace(phrase, "")
        
        cleaned = cleaned.strip()
        if not cleaned:
            return "I approach complex backend and agentic challenges from first principles—gathering evidence, weighing trade-offs, and shipping reliable systems."
        return cleaned

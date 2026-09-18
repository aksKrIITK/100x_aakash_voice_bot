import re
from typing import List, Dict, Any
from app.services.semantic_rag import semantic_rag_service
from app.personality.system_prompt import build_system_prompt_with_context
from app.services.llm_service import LLMService
from app.core.logging import logger


class AgenticPersonaPipeline:
    """Multi-stage Agentic Pipeline for context resolution, RAG retrieval, and persona generation."""

    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()
        self.rag = semantic_rag_service

    def resolve_context_query(self, user_message: str, history: List[Dict[str, str]]) -> str:
        """Stage 1: Context Resolver Agent. Resolves pronouns, follow-ups, and speech transcription artifacts."""
        cleaned = user_message.strip()
        lower = cleaned.lower()

        # 1. Voice transcription phonetic normalization
        phonetic_fixes = [
            (r'\b(?:take|text|track)\s+stack\b', 'tech stack skills technologies'),
            (r'\bothers?\s+(?:take|text)\s+stack\b', 'other technologies tech stack'),
            (r'\bwork(?:ed)?\s+don\'?t\b', 'worked on'),
            (r'\bwork\s*d\b', 'worked'),
            (r'\bwork\s+(?:at|in)?\s*experience\b', 'work experience worldref godizy'),
            (r'\bjob\s+experience\b', 'work experience worldref godizy'),
            (r'\b4\s+minute\b', '4 minute reporting query latency optimization'),
            (r'\bquery\s+fix\b', '4 minute unindexed query latency optimization worldref'),
            (r'\byour\s+team\b', 'lead backend team mentorship worldref'),
            (r'\bpaying\s+clients\b', 'godizy 10 paying smb customers'),
            (r'\bschool\b', 'education iit kanpur btech electrical engineering jnu'),
            (r'\bcollege\b', 'education iit kanpur jnu international politics'),
            (r'\bdegree\b', 'iit kanpur btech jnu ma international politics'),
            (r'\bwhat\s+skills\b', 'skills tech stack technologies'),
            (r'\bwhich\s+technolog(?:y|ies)\b', 'tech stack technologies frameworks'),
        ]
        for pat, rep in phonetic_fixes:
            if re.search(pat, lower):
                cleaned = re.sub(pat, rep, cleaned, flags=re.IGNORECASE)

        # 2. Contextual pronoun and follow-up detection
        follow_up_cues = [
            'why', 'how', 'tell me more', 'elaborate', 'that project', 'your team',
            'what happened', 'explain that', 'and then', 'what about', 'how about',
            'there', 'that', 'this', 'it', 'them', 'did you', 'was that', 'solve that',
            'handle that', 'the problem', 'the challenge', 'the hardest', 'hurdle',
            'bottleneck', 'optimization'
        ]
        
        has_pronoun_or_cue = any(
            re.search(r'\b' + re.escape(c) + r'\b', lower) for c in follow_up_cues
        )
        is_short = len(cleaned.split()) <= 6

        if (has_pronoun_or_cue or is_short) and history:
            # Look backwards through history for the last discussed topic
            last_context_text = ""
            for m in reversed(history):
                content = m.get("content", "")
                if content:
                    last_context_text += " " + content.lower()
                    if len(last_context_text) > 400:
                        break

            # Infer context domain
            if "worldref" in last_context_text or "rfq" in last_context_text:
                if any(w in lower for w in ['problem', 'challenge', 'difficult', 'hardest', 'solve', 'latency', 'optimize', 'there']):
                    cleaned += " WorldRef latency 4 minute query optimization problem unindexed SLA"
                elif any(w in lower for w in ['team', 'mentor', 'lead', 'culture', 'engineers']):
                    cleaned += " WorldRef backend microservices architecture mentorship team"
                else:
                    cleaned += " WorldRef backend architecture AI layer"
            elif "godizy" in last_context_text or "smb" in last_context_text or "customer" in last_context_text:
                cleaned += " Godizy founder SaaS SMB 10 paying customers"
            elif "enterprise ai" in last_context_text or "langgraph" in last_context_text or "worker" in last_context_text:
                cleaned += " LangGraph Enterprise AI Worker agentic platform pgvector MCP"
            elif "iit" in last_context_text or "jnu" in last_context_text or "upsc" in last_context_text:
                cleaned += " IIT Kanpur JNU education engineering civil services"

        return cleaned

    async def execute(self, user_message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Runs the complete agentic pipeline."""
        # 1. Context Resolution & Query Normalization
        resolved_query = self.resolve_context_query(user_message, history)

        # 2. Semantic RAG Retrieval
        top_chunks = self.rag.retrieve(resolved_query, top_k=2)
        grounding_context = self.rag.get_grounding_context(resolved_query, top_k=2)

        logger.info(f"Resolved query: '{resolved_query}' -> Top chunk: '{top_chunks[0][0]['topic']}' (score: {top_chunks[0][1]:.2f})")

        # 3. Persona Synthesis
        system_prompt = build_system_prompt_with_context(grounding_context)
        answer = await self.llm_service.generate_response(history, system_prompt)

        return {
            "resolved_query": resolved_query,
            "top_topic": top_chunks[0][0]["topic"],
            "top_score": top_chunks[0][1],
            "grounding_context": grounding_context,
            "answer": answer
        }


agentic_pipeline = AgenticPersonaPipeline()

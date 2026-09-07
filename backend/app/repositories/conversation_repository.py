import uuid
import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.models import ConversationModel, MessageModel
from app.core.logging import logger


class ConversationData:
    """In-memory conversation structure."""
    def __init__(self, conversation_id: str):
        self.id = conversation_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.messages: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str) -> Dict[str, Any]:
        msg = {
            "id": str(uuid.uuid4()),
            "conversation_id": self.id,
            "role": role,
            "content": content,
            "created_at": datetime.utcnow()
        }
        self.messages.append(msg)
        self.updated_at = datetime.utcnow()
        return msg


# Singleton in-memory storage dictionary
_in_memory_store: Dict[str, ConversationData] = {}
_lock = asyncio.Lock()


class ConversationRepository:
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session

    async def create_conversation(self, conversation_id: Optional[str] = None) -> str:
        cid = conversation_id or str(uuid.uuid4())
        
        if self.session:
            try:
                conv = ConversationModel(id=cid)
                self.session.add(conv)
                await self.session.commit()
                return cid
            except Exception as e:
                logger.warning(f"DB error during create_conversation: {e}. Using in-memory store.")

        async with _lock:
            _in_memory_store[cid] = ConversationData(cid)
        return cid

    async def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        if self.session:
            try:
                stmt = select(ConversationModel).options(selectinload(ConversationModel.messages)).filter_by(id=conversation_id)
                result = await self.session.execute(stmt)
                conv = result.scalar_one_or_none()
                if conv:
                    return {
                        "id": conv.id,
                        "created_at": conv.created_at,
                        "updated_at": conv.updated_at,
                        "messages": [
                            {
                                "id": m.id,
                                "conversation_id": m.conversation_id,
                                "role": m.role,
                                "content": m.content,
                                "created_at": m.created_at
                            }
                            for m in conv.messages
                        ]
                    }
            except Exception as e:
                logger.warning(f"DB error during get_conversation: {e}. Fallback to in-memory store.")

        async with _lock:
            conv_mem = _in_memory_store.get(conversation_id)
            if conv_mem:
                return {
                    "id": conv_mem.id,
                    "created_at": conv_mem.created_at,
                    "updated_at": conv_mem.updated_at,
                    "messages": conv_mem.messages
                }
        return None

    async def ensure_conversation(self, conversation_id: str) -> Dict[str, Any]:
        conv = await self.get_conversation(conversation_id)
        if not conv:
            await self.create_conversation(conversation_id)
            conv = await self.get_conversation(conversation_id)
            if not conv:
                # Fallback directly
                conv_mem = ConversationData(conversation_id)
                _in_memory_store[conversation_id] = conv_mem
                return {
                    "id": conv_mem.id,
                    "created_at": conv_mem.created_at,
                    "updated_at": conv_mem.updated_at,
                    "messages": conv_mem.messages
                }
        return conv

    async def add_message(self, conversation_id: str, role: str, content: str) -> Dict[str, Any]:
        await self.ensure_conversation(conversation_id)
        
        if self.session:
            try:
                msg_id = str(uuid.uuid4())
                msg_model = MessageModel(
                    id=msg_id,
                    conversation_id=conversation_id,
                    role=role,
                    content=content
                )
                self.session.add(msg_model)
                await self.session.commit()
                return {
                    "id": msg_id,
                    "conversation_id": conversation_id,
                    "role": role,
                    "content": content,
                    "created_at": datetime.utcnow()
                }
            except Exception as e:
                logger.warning(f"DB error during add_message: {e}. Using in-memory store.")

        async with _lock:
            if conversation_id not in _in_memory_store:
                _in_memory_store[conversation_id] = ConversationData(conversation_id)
            return _in_memory_store[conversation_id].add_message(role, content)

    async def get_messages(self, conversation_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        conv = await self.get_conversation(conversation_id)
        if not conv or "messages" not in conv:
            return []
        messages = conv["messages"]
        return messages[-limit:]

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_chat_flow_and_history():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create conversation
        conv_res = await ac.post("/api/v1/conversations")
        assert conv_res.status_code == 200
        cid = conv_res.json()["conversation_id"]

        # First question (superpower)
        chat1 = await ac.post(
            "/api/v1/chat",
            json={"conversation_id": cid, "message": "What is your #1 superpower?"}
        )
        assert chat1.status_code == 200
        ans1 = chat1.json()["answer"]
        assert len(ans1) > 0
        assert "superpower" in ans1.lower() or "learning" in ans1.lower()

        # Follow up question
        chat2 = await ac.post(
            "/api/v1/chat",
            json={"conversation_id": cid, "message": "Can you give an example of that?"}
        )
        assert chat2.status_code == 200
        ans2 = chat2.json()["answer"]
        assert len(ans2) > 0


@pytest.mark.asyncio
async def test_invalid_chat_request():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/chat", json={"conversation_id": "", "message": ""})
    assert response.status_code == 422  # Validation error

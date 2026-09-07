import io
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_voice_chat_endpoint_valid():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        conv_res = await ac.post("/api/v1/conversations")
        cid = conv_res.json()["conversation_id"]

        dummy_audio = b"RIFF....WAVEfmt ....data...."
        files = {"audio": ("recording.wav", io.BytesIO(dummy_audio), "audio/wav")}
        data = {"conversation_id": cid}

        response = await ac.post("/api/v1/voice/chat", files=files, data=data)
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["conversation_id"] == cid
        assert "transcript" in res_json
        assert "answer" in res_json


@pytest.mark.asyncio
async def test_voice_chat_invalid_file():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = {"audio": ("test.exe", io.BytesIO(b"binary"), "application/x-msdownload")}
        data = {"conversation_id": "test-uuid"}
        response = await ac.post("/api/v1/voice/chat", files=files, data=data)
        assert response.status_code == 400

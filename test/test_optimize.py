# test_optimize.py
import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app  # or wherever your FastAPI app is defined

@pytest.mark.asyncio
async def test_optimize_prompt_success():
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "prompt": "What is a black hole?",
            "response": "A black hole forms when a massive star collapses, creating gravity so strong not even light can escape."
        }

        response = await client.post("/optimize", json=payload)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Basic output validations
        assert "optimized_prompt" in data
        assert "score" in data
        assert "total_score" in data
        assert "explanation" in data
        assert "root_cause" in data
        assert "prompt_id" in data
        assert "timestamp" in data

        # Score structure check
        assert all(key in data["score"] for key in ["clarity", "structure", "detail"])

@pytest.mark.asyncio
async def test_optimize_prompt_validation_error():
    async with AsyncClient(app=app, base_url="http://test") as client:
        bad_payload = {
            "prompt": "",  # Missing required data
            "response": ""
        }

        response = await client.post("/optimize", json=bad_payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

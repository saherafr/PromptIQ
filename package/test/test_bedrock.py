# test_bedrock.py

import asyncio
from app.services.bedrock_client import call_claude_with_retry

async def main():
    payload = {
    "anthropic_version": "bedrock-2023-05-31",
    "messages": [
        {
            "role": "user",
            "content": "Explain what is a circuit breaker in backend systems."
        }
    ],
    "max_tokens": 1024,
    "temperature": 0.7
}


    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"


    response = await call_claude_with_retry(payload, model_id)
    print("Response from Claude:\n", response)

if __name__ == "__main__":
    asyncio.run(main())

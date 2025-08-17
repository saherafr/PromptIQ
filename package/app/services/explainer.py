import asyncio
from app.services.bedrock_client import call_claude_with_retry

# Step 1: Define system prompt
SYSTEM_PROMPT = (
    "You are a helpful prompt engineering tutor. Your job is to explain how well a prompt guided the AI's response. "
    "Break down the prompt's clarity, tone, specificity, and structure. Give a brief explanation (3–5 sentences) "
    "so the user can learn to write better prompts."
)

# Step 2: Format the user input
def build_user_prompt(prompt: str, response: str) -> str:
    return f"""
Analyze the following prompt and its AI-generated response.

<prompt>
{prompt}
</prompt>

<response>
{response}
</response>

Explain how the prompt influenced the response, and suggest any improvements.
"""

# Step 3: Create Bedrock-compatible payload
def build_payload(prompt: str, response: str) -> dict:
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": build_user_prompt(prompt, response)}
        ],
        "max_tokens": 512,
        "temperature": 0.5
    }

# Step 4: Async function to fetch explanation
async def get_prompt_explanation(prompt: str, response: str) -> dict:
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    payload = build_payload(prompt, response)
    return await call_claude_with_retry(payload, model_id)

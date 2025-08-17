import asyncio
import json
from app.services.bedrock_client import call_claude_with_retry

SYSTEM_PROMPT = (
    "You are a prompt diagnostics expert. Given a user prompt, detect any issues such as vagueness, ambiguity, poor structure, or redundancy. "
    "Then offer 1-2 specific suggestions for making it clearer and more effective."
)

def build_user_prompt(prompt: str) -> str:
    return f"""
Analyze the following prompt for weaknesses and suggest improvements.

<prompt>
{prompt}
</prompt>

Return your answer in this JSON format:
{{
  "issues": [str],
  "suggestion": str
}}
"""

def build_payload(prompt: str) -> dict:
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": build_user_prompt(prompt)}
        ],
        "max_tokens": 512,
        "temperature": 0.4
    }



async def analyze_prompt(prompt: str) -> dict:
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    payload = build_payload(prompt)
    result = await call_claude_with_retry(payload, model_id)

    try:
        return json.loads(result["output"])
    except Exception:
        return {
            "issues": ["Could not parse Claude output."],
            "suggestion": prompt  # fallback to original prompt
        }


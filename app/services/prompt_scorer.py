#accept a prompt str
#send to claude via bedrock
#return score breakdown and ans
import json
import asyncio
from app.services.bedrock_client import call_claude_with_retry
SYSTEM_PROMPT = (
    "You are a strict AI evaluation assistant. Your job is to score the quality of LLM-generated responses "
    "using the following criteria: clarity, structure, relevance. Each should be rated from 1 to 10. "
    "You must also provide an overall score and 1-2 lines of constructive feedback."
)
 # JSON score on clarity, struc, relevance and feedback
 #usser promt-task
def build_user_prompt(prompt: str, response: str) -> str:
        return f"""
    Evaluate the following LLM output.

    <prompt>
    {prompt}
    </prompt>

    <response>
    {response}
    </response>

    Give your answer in this JSON format:
    {{
    "clarity": int,
    "structure": int,
    "relevance": int,
    "overall_score": int,
    "feedback": str
    }}
    """
def build_payload(prompt: str, response: str) -> dict:
    user_input = f"""
You are a strict AI evaluation assistant. Score the following AI response using these criteria: clarity, structure, relevance. Provide scores (1-10) and a short feedback in this JSON format:

{{
  "clarity": int,
  "structure": int,
  "relevance": int,
  "overall_score": int,
  "feedback": str
}}

<prompt>
{prompt}
</prompt>

<response>
{response}
</response>
"""

    return {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": user_input.strip()
            }
        ],
        "max_tokens": 512,
        "temperature": 0.3
    }

async def score_prompt_response(prompt: str, response: str) -> dict:
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    payload = build_payload(prompt, response)
    raw_result = await call_claude_with_retry(payload, model_id)
    return json.loads(raw_result["output"])


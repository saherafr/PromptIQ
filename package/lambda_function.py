import json
from app.services.analyzer import analyze_prompt
from app.services.prompt_scorer import score_prompt_response
from app.services.explainer import get_prompt_explanation
import asyncio

def lambda_handler(event, context):
    """Single entry point. event['action'] decides what to run."""
    action = event.get("action", "analyze")
    prompt = event.get("prompt", "")
    response = event.get("response", "")

    if not prompt:
        return _reply(400, {"error": "prompt is required"})

    if action == "analyze":
        result = asyncio.run(analyze_prompt(prompt))
        return _reply(200, result)

    if action == "score":
        if not response:
            return _reply(400, {"error": "response is required for scoring"})
        result = asyncio.run(score_prompt_response(prompt, response))
        return _reply(200, result)

    if action == "explain":
        if not response:
            return _reply(400, {"error": "response is required for explanation"})
        result = asyncio.run(get_prompt_explanation(prompt, response))
        return _reply(200, {"output": result["output"]})

    return _reply(400, {"error": f"unknown action '{action}'"})

def _reply(code, body):
    return {"statusCode": code, "body": json.dumps(body)}

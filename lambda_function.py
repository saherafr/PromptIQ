import json
import asyncio
from app.services.analyzer import analyze_prompt
from app.services.prompt_scorer import score_prompt_response
from app.services.explainer import get_prompt_explanation

# ---- helpers ----
def respond(code, obj):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(obj)
    }

def parse_event(event):
    """
    Support:
      - direct Lambda test (keys at top level)
      - API Gateway HTTP API / REST (JSON string in event['body'])
      - preflight OPTIONS
    """
    # Handle preflight
    if event.get("httpMethod") == "OPTIONS":
        return "options", {}, ""

    body = event.get("body")
    if isinstance(body, str):
        try:
            payload = json.loads(body or "{}")
        except json.JSONDecodeError:
            payload = {}
    elif isinstance(body, dict):
        payload = body
    else:
        # direct invoke
        payload = event

    action = payload.get("action", "analyze")
    prompt = payload.get("prompt", "")
    response = payload.get("response", "")
    return action, {"prompt": prompt, "response": response}, payload

# ---- handler ----
def lambda_handler(event, context):
    action, data, raw_payload = parse_event(event)

    if action == "options":
        return respond(200, {})  # CORS preflight quick exit

    prompt = data["prompt"]
    response_txt = data["response"]

    if not prompt:
        return respond(400, {"error": "prompt is required"})

    try:
        if action == "analyze":
            result = asyncio.run(analyze_prompt(prompt))
            return respond(200, result)

        if action == "score":
            if not response_txt:
                return respond(400, {"error": "response is required for scoring"})
            result = asyncio.run(score_prompt_response(prompt, response_txt))
            return respond(200, result)

        if action == "explain":
            if not response_txt:
                return respond(400, {"error": "response is required for explanation"})
            result = asyncio.run(get_prompt_explanation(prompt, response_txt))
            return respond(200, {"output": result["output"]})

        return respond(400, {"error": f"unknown action '{action}'"})

    except Exception as e:
        # optional: log stack trace
        return respond(500, {"error": "internal error", "detail": str(e)})

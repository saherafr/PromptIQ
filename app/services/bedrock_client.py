# Purpose: Handle safe, fault-tolerant, and scalable communication with Claude (via AWS Bedrock)
# Patterns used: Retry, Circuit Breaker, Thread Isolation

import boto3  # AWS SDK for Bedrock
import json
import asyncio
from pybreaker import CircuitBreaker
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# --- Custom Error Type ---

class ClaudeError(Exception):
    """
    Custom exception to distinguish retry-safe Claude-related errors
    (e.g., timeouts, internal server errors) from user input bugs (e.g., ValueError).
    """
    pass


# --- Circuit Breaker Configuration ---

claude_breaker = CircuitBreaker(
    fail_max=3,               # Allow 3 consecutive failures
    reset_timeout=20,         # Wait 20s before trying again
    exclude=[ValueError]      # Don't trip the breaker for user-caused errors
)


# --- Claude API Call (Sync) ---

@retry(
    stop=stop_after_attempt(3),                               # Try up to 3 times
    wait=wait_exponential(multiplier=1, min=1, max=8),        # Backoff: 1s → 2s → 4s → ...
    retry=retry_if_exception_type(ClaudeError)                # Only retry infra errors
)
@claude_breaker
def _invoke_claude(payload: dict, model_id: str) -> dict:
    try:
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

        response = bedrock.invoke_model_with_response_stream(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )

        # Combine streaming chunks into final output
        full_response = ""
        for event in response['body']:
            chunk_info = event.get("chunk")
            if not chunk_info:
                continue

            # Decode and parse JSON from chunk
            decoded = json.loads(chunk_info["bytes"].decode("utf-8"))

            # Extract streaming delta safely
            delta = decoded.get("delta", {})
            text_piece = delta.get("text", "")

            full_response += text_piece

        return {"output": full_response}

    except Exception as e:
        print(f"[ClaudeError] Claude invocation failed: {e}")
        raise ClaudeError("Claude call failed")


# --- Async Wrapper ---

async def call_claude_with_retry(payload: dict, model_id: str) -> dict:
    """
    Async-friendly wrapper to call Claude in a background thread.
    Keeps your FastAPI app non-blocking.
    """
    return await asyncio.to_thread(_invoke_claude, payload, model_id)

# test_scorer.py
import asyncio
from app.services.prompt_scorer import score_prompt_response

async def main():
    prompt = "What is a black hole?"
    response = "A black hole is formed when gravity pulls so much matter together that even light can't escape it."

    score = await score_prompt_response(prompt, response)
    print("Claude's evaluation:", score)

asyncio.run(main())

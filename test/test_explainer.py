# test_explainer.py
import asyncio
from app.services.explainer import get_prompt_explanation

async def main():
    prompt = "What is a black hole?"
    response = "A black hole is formed when gravity pulls so much matter together that even light can't escape it."

    explanation = await get_prompt_explanation(prompt, response)
    print("Explanation:", explanation)

asyncio.run(main())

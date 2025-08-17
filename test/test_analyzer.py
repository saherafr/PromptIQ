import asyncio
from app.services.analyzer import analyze_prompt

async def main():
    prompt = "Tell me about history."
    result = await analyze_prompt(prompt)
    print("Prompt issues analysis:", result)

asyncio.run(main())

from pydantic import BaseModel
from typing import Dict

class PromptRecord(BaseModel):
    prompt_id: str
    prompt: str
    response: str
    optimized_prompt: str
    score: Dict[str, int]
    total_score: int
    explanation: str
    root_cause: str
    timestamp: str

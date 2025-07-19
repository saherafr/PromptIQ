from pydantic import BaseModel
from typing import Dict 
class PromptResponse(BaseModel):
    optimized_prompt: str
    score: Dict[str, int]
    total_score: int
    explanation: str
    root_cause: str
    prompt_id: str
    timestamp: str
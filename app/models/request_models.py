from pydantic import BaseModel
from typing import Literal
from pydantic import Field

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=5)
    response: str = Field(..., min_length=5)
    mode: Literal["refine", "summarize", "elaborate"]
    debug: bool = False

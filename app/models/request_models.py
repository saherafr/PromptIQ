 from pydantic import BaseModel
 from typing import Literal
 class PromptRequest(BaseModel):
     prompt:str
     mode: Literal["refine", "summarize","elaborate"]
     debug: bool= False
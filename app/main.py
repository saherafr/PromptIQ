from fastapi import FastAPI
from app.api.v1.routes import optimize

app = FastAPI(title="PromptEngineer API")

app.include_router(optimize.router, prefix="/api/v1")

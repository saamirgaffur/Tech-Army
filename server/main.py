from fastapi import FastAPI
from api import prompt

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(prompt.router, prefix="/prompt", tags=["prompt"])
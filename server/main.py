from fastapi import FastAPI
from server.api import prompt

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(prompt.router, prefix="/prompt", tags=["prompt"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import prompt

app = FastAPI()

# CORS Configuration for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(prompt.router, prefix="/prompt", tags=["prompt"])
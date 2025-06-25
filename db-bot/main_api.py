from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_handler import search_qdrant
from openai_handler import generate_answer

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

# Define the response model for the bot's reply
class QueryResponse(BaseModel):
    response: str 

@app.post("/ask", tags=["Chatbot"])
async def ask_question(request: QueryRequest):
    try:
        search_results = search_qdrant(query=request.question)

        if not search_results:
            return QueryResponse(response="No relevant data found.")

        answer = generate_answer(request.question, search_results)
        print(f"Generated answer: {answer}")
        return QueryResponse(response=answer) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {e}")

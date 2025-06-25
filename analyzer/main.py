from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend import handle_user_query  # Importing the main chatbot function from backend.py

app = FastAPI()

# Define the request model for the incoming user query
class QueryRequest(BaseModel):
    user_query: str

# Define the response model for the bot's reply
class QueryResponse(BaseModel):
    response: str

@app.post("/chatbot/", response_model=QueryResponse)
async def chat_with_bot(query: QueryRequest):
    try:
        # Call the function from backend.py to process the user query
        response = handle_user_query(query.user_query)
        return QueryResponse(response=response)
    except Exception as e:
        # If something goes wrong, return an error message
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))



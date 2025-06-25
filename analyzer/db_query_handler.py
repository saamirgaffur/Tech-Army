import httpx

async def handle_db_query(user_query: str) -> str:
    # Prepare the request payload
    payload = {
        "question": user_query
    }

    # Make the API request to the FastAPI endpoint
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
            response = await client.post("http://127.0.0.1:8002/ask", json=payload)

            # Check if the response was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "No response in the data.")
            else:
                return f"Error: Unable to fetch data (Status code: {response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

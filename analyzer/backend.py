from intent_classifier import classify_intent
from faq_static_bot import handle_static_response
from db_query_handler import handle_db_query

async def handle_user_query(user_query: str):
    intent = classify_intent(user_query)
    print(f"[Intent Detected]: {intent}")

    if intent == "static_response":
        return handle_static_response(user_query)
    
    elif intent == "db_query":
        return await handle_db_query(user_query)

    else:
        return "Sorry, I couldn't understand your query."

# CLI runner
if __name__ == "__main__":
    print("Chatbot running. Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = handle_user_query(user_input)
        print("Bot:", result)

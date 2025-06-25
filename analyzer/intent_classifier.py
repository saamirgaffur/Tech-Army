import openai
import os
from dotenv import load_dotenv
import openai

# Load .env file
load_dotenv()

# Get the key from env
openai.api_key = os.getenv("OPENAI_API_KEY")

INTENTS = ["static_response", "db_query", "fallback"]

def classify_intent(user_query: str) -> str:
    prompt = f"""
You are an intent classifier for an internal chatbot. Classify each user message into one of the following:

static_response → greetings (hi, hello, hey) or questions about what the chatbot does or company FAQs  
db_query        → any query asking for information from a database (e.g., employees, projects, trainings, skills, shifts)  
fallback        → irrelevant, joke, random or unrecognized queries

Message: "{user_query}"

Return only one: static_response, db_query, or fallback.
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You classify chatbot queries into one of three intents."},
            {"role": "user", "content": prompt}
        ]
    )

    intent = response.choices[0].message.content.strip().lower()
    return intent if intent in INTENTS else "fallback"

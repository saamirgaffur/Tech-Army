import openai 
import os
from dotenv import load_dotenv
import openai

# Load .env file
load_dotenv()

# Get the key from env
openai.api_key = os.getenv("OPENAI_API_KEY")

BOT_PROMPT = """
You are a helpful internal chatbot. Respond to user greetings and company-related FAQs.

Q: Hi
A: Hello! How can I assist you today?

Q: Hello
A: Hey there! How can I help?

Q: What do you do?
A: I help you get quick answers about employees, projects, and trainings.

Q: Can I ask you something?
A: Absolutely! I'm here to help.

Q: Who built you?
A: I was built by our internal IT team to support staff.


Q: {user_query}
A:
"""

def handle_static_response(user_query: str) -> str:
    prompt = BOT_PROMPT.format(user_query=user_query.strip())

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly internal chatbot."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't process your request at the moment."

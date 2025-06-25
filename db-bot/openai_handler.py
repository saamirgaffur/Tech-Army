import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL")

def generate_answer(question, documents):
    context = "\n---\n".join([doc['text'] for doc in documents])

    prompt = f"""
You are an assistant that answers questions about employees, their projects, skills, and trainings based on the following context.

Context:
{context}

Question: {question}

Instructions:
- If the question includes a specific EmployeeID , ProjectID, or TrainingID, retrieve and summarize details about that entity.
- If the question asks about what projects or trainings an employee is involved in, list them clearly.
- If the question is about skills, return the list of skills associated with the employee(s).
- If no specific ID is mentioned, summarize relevant matches from the context.
- Keep the response structured, precise, and human-readable.
- Answer all the questions based on Age,Name etc... 

Answer:
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

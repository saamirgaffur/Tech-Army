from openai import OpenAI
from dotenv import load_dotenv
from supabase_handler import fetch_joined_data
from qdrant_handler import upsert_documents
import os
from tqdm import tqdm

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("EMBEDDING_MODEL")

def join_to_text(entry):
    emp = entry["employee"]
    projects = entry["projects"]
    trainings = entry["trainings"]

    emp_text = (
        f"Employee ID: {emp.get('employee_id')}\n"
        f"Name: {emp.get('name')}\n"
        f"Age: {emp.get('age')}\n"
        f"Address: {emp.get('address')}\n"
        f"Designation: {emp.get('designation')}\n"
        f"Shift: {emp.get('shift')}\n"
        f"Skills: {', '.join(emp.get('skills') or [])}\n"
    )

    project_text = "\n".join([
        f"- ProjectID: {p.get('project_id')}, Name: {p.get('project_name')}, "
        f"Type: {p.get('project_type')}, Category: {p.get('project_category')}, "
        f"Tech Stack: {', '.join(p.get('tech_stack') or [])}"
        for p in projects
    ]) or "No project records available."

    training_text = "\n".join([
        f"- TrainingID: {t.get('training_id')}, Topic: {t.get('train_topic')}"
        for t in trainings
    ]) or "No training records available."

    return f"""
==== Employee Info ====
{emp_text}
==== Project Involvement ====
{project_text}
==== Trainings Attended ====
{training_text}
"""

def batch_upload(docs, batch_size=10):
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        try:
            upsert_documents(batch)
            print(f"Uploaded batch {i // batch_size + 1}: {len(batch)} docs")
        except Exception as e:
            print(f"Error uploading batch {i // batch_size + 1}: {e}")

def embed_and_store():
    data = fetch_joined_data()
    docs = []

    for i, entry in enumerate(tqdm(data, desc="Embedding employee data")):
        try:
            text = join_to_text(entry)
            embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
            docs.append({
                "id": i,
                "vector": embedding,
                "payload": {
                    "text": text,
                    "metadata": {
                        "EmployeeID": entry['employee'].get('employee_id'),
                        "ProjectIDs": [p["project_id"] for p in entry["projects"]],
                        "TrainingIDs": [t["training_id"] for t in entry["trainings"]]
                    }
                }
            })
        except Exception as e:
            print(f"Error embedding entry {i}: {e}")

    if docs:
        batch_upload(docs, batch_size=10)
        print(f"Successfully embedded and upserted {len(docs)} documents.")
    else:
        print("No documents were processed.")

if __name__ == "__main__":
    embed_and_store()

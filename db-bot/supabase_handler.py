from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def fetch_joined_data():
    employees = supabase.table("employee").select("*").execute().data
    projects = supabase.table("project").select("*").execute().data
    project_employees = supabase.table("project_employee").select("*").execute().data
    trainings = supabase.table("training").select("*").execute().data
    training_employees = supabase.table("training_employee").select("*").execute().data

    enriched = []
    for emp in employees:
        emp_id = emp["employee_id"]

        related_proj_ids = [pe["project_id"] for pe in project_employees if pe["employee_id"] == emp_id]
        related_projects = [p for p in projects if p["project_id"] in related_proj_ids]

        related_train_ids = [te["training_id"] for te in training_employees if te["employee_id"] == emp_id]
        related_trainings = [t for t in trainings if t["training_id"] in related_train_ids]

        enriched.append({
            "employee": emp,
            "projects": related_projects,
            "trainings": related_trainings
        })
    return enriched

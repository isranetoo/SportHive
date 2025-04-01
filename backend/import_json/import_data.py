import json
import sys
import os

# Adicionar o diretório do backend ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import SessionLocal, Base  # Import Base for schema creation
from models import Sport  

def load_json():
    # Use absolute path to the JSON file to avoid path issues
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/sports.json"))
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        # Debug: Print the structure of the first sport object
        if data and len(data) > 0:
            print("First sport object structure:", data[0])
        return data

def create_schema():
    # Create the database schema if it doesn't exist
    engine = create_engine("postgresql://postgres:tynHliQsLhPtOCwSenRiwVOpQUfYYzdY@maglev.proxy.rlwy.net:23557/railway")  # Replace with your DB connection string
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema created (if not already existing).")

def insert_data():
    db: Session = SessionLocal()
    sports_data = load_json()
    
    for sport in sports_data:
        sport_name = sport["name"]
        sport_category = sport.get("category", "Não categorizado")  # Default if missing
        
        print(f"Importing: {sport_name} (Category: {sport_category})")
        db.add(Sport(name=sport_name, category=sport_category))

    db.commit()
    db.close()

if __name__ == "__main__":
    create_schema()  # Ensure schema is created before inserting data
    insert_data()
    print("✅ Dados importados para o PostgreSQL!")

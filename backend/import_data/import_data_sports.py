import json
import sys
import os
import argparse

# Adicionar o diretório do backend ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from database import SessionLocal, Base  # Import Base for schema creation
from models import Sport  

def load_json():
    # Define paths
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
    json_path = os.path.join(data_dir, "sports.json")
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        print(f"Creating data directory at: {data_dir}")
        os.makedirs(data_dir)
    
    # Check if the file exists
    if not os.path.exists(json_path):
        print(f"Warning: sports.json not found at {json_path}")
        print("Creating a sample sports.json file...")
        # Create a sample sports.json file with minimal data
        sample_data = [
            {
                "name": "Futebol",
                "category": "Coletivo",
                "description": "Esporte coletivo jogado entre duas equipes de 11 jogadores cada.",
                "image": "futebol.jpg"
            },
            {
                "name": "Basquete",
                "category": "Coletivo",
                "description": "Esporte jogado entre duas equipes de 5 jogadores cada.",
                "image": "basquete.jpg"
            }
        ]
        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(sample_data, file, ensure_ascii=False, indent=4)
    
    # Now we can safely open the file
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Debug: Print the structure of the first sport object
            if data and len(data) > 0:
                print("First sport object structure:", data[0])
            return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

def create_schema(drop_existing=False):
    # Create the database schema if it doesn't exist
    engine = create_engine("postgresql://postgres:tynHliQsLhPtOCwSenRiwVOpQUfYYzdY@maglev.proxy.rlwy.net:23557/railway")
    
    inspector = inspect(engine)
    
    # Check if sports table exists and has the right columns
    if "sports" in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('sports')]
        missing_columns = []
        for expected_col in ['name', 'category', 'description', 'image']:
            if expected_col not in columns:
                missing_columns.append(expected_col)
        
        if missing_columns:
            print(f"Table 'sports' exists but is missing columns: {', '.join(missing_columns)}")
            if drop_existing:
                print("Dropping tables to recreate schema...")
                Base.metadata.drop_all(bind=engine)
            else:
                print("⚠️ Missing columns detected but --recreate-schema flag not set.")
                print("Either:")
                print("1. Run this script with --recreate-schema flag to drop and recreate all tables")
                print("2. Manually alter the table to add the missing columns")
                sys.exit(1)  # Exit with error code
        else:
            print("Table 'sports' exists with all required columns.")
    else:
        print("Table 'sports' doesn't exist. Creating all tables...")
            
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema created/updated successfully.")

def insert_data():
    db: Session = SessionLocal()
    sports_data = load_json()
    
    # Get existing sports to avoid duplicates
    existing_sports = {sport.name.lower(): sport for sport in db.query(Sport).all()}
    
    inserted_count = 0
    skipped_count = 0
    
    for sport in sports_data:
        sport_name = sport["name"]
        sport_category = sport.get("category", "Não categorizado")  # Default if missing
        sport_description = sport.get("description", "")  # Default if missing
        sport_image = sport.get("image", "")  # Default if missing
        
        # Check if the sport already exists (case-insensitive comparison)
        if sport_name.lower() in existing_sports:
            print(f"Pulando: {sport_name} - Já existe no banco de dados.")
            skipped_count += 1
        else:
            print(f"Importando: {sport_name} (Categoria: {sport_category})")
            db.add(Sport(
                name=sport_name, 
                category=sport_category,
                description=sport_description,
                image=sport_image
            ))
            inserted_count += 1

    db.commit()
    db.close()
    
    print(f"\nResumo da importação:")
    print(f"✅ {inserted_count} esportes novos importados")
    print(f"⏩ {skipped_count} esportes pulados (já existiam)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import sports data to PostgreSQL database')
    parser.add_argument('--recreate-schema', action='store_true', 
                        help='Drop and recreate the database schema (WARNING: deletes all data)')
    args = parser.parse_args()
    
    create_schema(drop_existing=args.recreate_schema)  # Pass the argument to control schema recreation
    insert_data()
    print("✅ Dados importados para o PostgreSQL!")
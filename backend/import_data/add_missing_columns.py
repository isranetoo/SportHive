import sys
import os
from sqlalchemy import create_engine, text, inspect

# Adicionar o diretório do backend ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def add_missing_columns():
    """Add missing columns to existing tables without dropping them"""
    print("Checking for missing columns...")
    
    # Connect to database
    engine = create_engine("postgresql://postgres:tynHliQsLhPtOCwSenRiwVOpQUfYYzdY@maglev.proxy.rlwy.net:23557/railway")
    conn = engine.connect()
    
    try:
        # Check for sports table
        inspector = inspect(engine)
        
        if "sports" in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('sports')]
            missing_columns = []
            
            # Define expected columns with their types
            expected_columns = {
                'name': 'VARCHAR',
                'category': 'VARCHAR',
                'description': 'VARCHAR',
                'image': 'VARCHAR'
            }
            
            # Check which columns are missing
            for col_name, col_type in expected_columns.items():
                if col_name not in columns:
                    missing_columns.append((col_name, col_type))
            
            # Add missing columns
            if missing_columns:
                print(f"Found {len(missing_columns)} missing columns in sports table")
                for col_name, col_type in missing_columns:
                    nullable = "NULL" if col_name in ["description", "image"] else "NOT NULL DEFAULT ''"
                    sql = f"ALTER TABLE sports ADD COLUMN {col_name} {col_type} {nullable}"
                    print(f"Executing: {sql}")
                    conn.execute(text(sql))
                conn.commit()
                print("✅ Added all missing columns to sports table")
            else:
                print("✅ No missing columns in sports table")
        else:
            print("❌ Sports table doesn't exist. Run the import_data_sports.py script first.")
            
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_missing_columns()

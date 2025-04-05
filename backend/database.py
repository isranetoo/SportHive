import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text

# Verificar o ambiente através de variável de ambiente
USE_SQLITE = os.getenv("USE_SQLITE", "False").lower() in ("true", "1", "t")

# Configuração do banco de dados
if USE_SQLITE:
    # SQLite para desenvolvimento local/testes
    SQLITE_DATABASE_URL = "sqlite:///./sport_hive.db"
    engine = create_engine(
        SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL para produção
    DATABASE_URL = "postgresql://postgres:tynHliQsLhPtOCwSenRiwVOpQUfYYzdY@maglev.proxy.rlwy.net:23557/railway"
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa o banco de dados criando todas as tabelas definidas"""
    Base.metadata.create_all(bind=engine)

def recreate_db():
    """Recria todas as tabelas, apagando as existentes primeiro"""
    # Drop all tables first
    Base.metadata.drop_all(bind=engine)
    
    # For PostgreSQL, we need to manually drop sequences to avoid conflicts
    if not USE_SQLITE:
        conn = engine.connect()
        try:
            # Get a list of sequences that might be left over
            result = conn.execute(text(
                "SELECT relname FROM pg_class WHERE relkind = 'S' AND relname LIKE '%_id_seq'"
            ))
            sequences = [row[0] for row in result]
            
            # Drop each sequence
            for seq in sequences:
                conn.execute(text(f"DROP SEQUENCE IF EXISTS {seq} CASCADE"))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error dropping sequences: {e}")
        finally:
            conn.close()
    
    # Now create all tables
    Base.metadata.create_all(bind=engine)

def table_has_column(table_name, column_name):
    """Verifica se uma tabela possui determinada coluna"""
    inspector = inspect(engine)
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    return column_name in columns

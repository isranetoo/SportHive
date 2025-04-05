import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

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

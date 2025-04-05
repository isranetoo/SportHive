"""
Script para migrar o banco de dados existente para o novo esquema
sem perder os dados existentes
"""

from sqlalchemy import create_engine, text, Column, Integer, String, Float, MetaData, Table
from database import engine

def run_migrations():
    """
    Executa as migrações necessárias para atualizar o banco de dados
    sem perder os dados existentes
    """
    print("Iniciando migração do banco de dados...")
    
    # Conectar ao banco de dados
    conn = engine.connect()
    
    try:
        # Verificar se a tabela player_tournament existe
        try:
            conn.execute(text("SELECT 1 FROM player_tournament LIMIT 1"))
            player_tournament_exists = True
        except Exception:
            player_tournament_exists = False
            
        if player_tournament_exists:
            # Adicionar as novas colunas se a tabela já existir
            new_columns = [
                {"name": "losses", "type": "INTEGER", "default": 0},
                {"name": "hard_court_wins", "type": "INTEGER", "default": 0},
                {"name": "clay_court_wins", "type": "INTEGER", "default": 0},
                {"name": "grass_court_wins", "type": "INTEGER", "default": 0},
                {"name": "carpet_court_wins", "type": "INTEGER", "default": 0},
                {"name": "indoor_wins", "type": "INTEGER", "default": 0},
                {"name": "outdoor_wins", "type": "INTEGER", "default": 0},
                {"name": "elo_rating", "type": "FLOAT", "default": 1500.0}
            ]
            
            for column in new_columns:
                try:
                    # Verificar se a coluna já existe
                    conn.execute(text(f"SELECT {column['name']} FROM player_tournament LIMIT 1"))
                    print(f"Coluna {column['name']} já existe na tabela player_tournament.")
                except Exception:
                    # Adicionar a coluna se não existir
                    conn.execute(text(
                        f"ALTER TABLE player_tournament ADD COLUMN IF NOT EXISTS {column['name']} {column['type']} DEFAULT {column['default']}"
                    ))
                    print(f"Coluna {column['name']} adicionada à tabela player_tournament.")
        
        # Criar tabela player_vs_player se não existir
        try:
            conn.execute(text("SELECT 1 FROM player_vs_player LIMIT 1"))
            print("Tabela player_vs_player já existe.")
        except Exception:
            conn.execute(text("""
                CREATE TABLE player_vs_player (
                    id SERIAL PRIMARY KEY,
                    player1_id INTEGER NOT NULL REFERENCES players(id),
                    player2_id INTEGER NOT NULL REFERENCES players(id),
                    total_matches INTEGER DEFAULT 0,
                    player1_wins INTEGER DEFAULT 0,
                    player2_wins INTEGER DEFAULT 0,
                    hard_court_matches INTEGER DEFAULT 0,
                    hard_court_player1_wins INTEGER DEFAULT 0,
                    hard_court_player2_wins INTEGER DEFAULT 0,
                    clay_court_matches INTEGER DEFAULT 0,
                    clay_court_player1_wins INTEGER DEFAULT 0,
                    clay_court_player2_wins INTEGER DEFAULT 0,
                    grass_court_matches INTEGER DEFAULT 0,
                    grass_court_player1_wins INTEGER DEFAULT 0,
                    grass_court_player2_wins INTEGER DEFAULT 0,
                    carpet_court_matches INTEGER DEFAULT 0,
                    carpet_court_player1_wins INTEGER DEFAULT 0,
                    carpet_court_player2_wins INTEGER DEFAULT 0,
                    indoor_matches INTEGER DEFAULT 0,
                    indoor_player1_wins INTEGER DEFAULT 0,
                    indoor_player2_wins INTEGER DEFAULT 0,
                    outdoor_matches INTEGER DEFAULT 0,
                    outdoor_player1_wins INTEGER DEFAULT 0,
                    outdoor_player2_wins INTEGER DEFAULT 0
                )
            """))
            print("Tabela player_vs_player criada.")
        
        # Criar tabela player_elo se não existir
        try:
            conn.execute(text("SELECT 1 FROM player_elo LIMIT 1"))
            print("Tabela player_elo já existe.")
        except Exception:
            conn.execute(text("""
                CREATE TABLE player_elo (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER NOT NULL REFERENCES players(id),
                    elo_rating FLOAT DEFAULT 1500.0,
                    hard_court_elo FLOAT DEFAULT 1500.0,
                    clay_court_elo FLOAT DEFAULT 1500.0,
                    grass_court_elo FLOAT DEFAULT 1500.0,
                    carpet_court_elo FLOAT DEFAULT 1500.0,
                    indoor_elo FLOAT DEFAULT 1500.0,
                    outdoor_elo FLOAT DEFAULT 1500.0,
                    active BOOLEAN DEFAULT TRUE,
                    last_updated DATE NULL
                )
            """))
            print("Tabela player_elo criada.")
        
        conn.commit()
        print("Migração concluída com sucesso!")
        
    except Exception as e:
        conn.rollback()
        print(f"Erro durante a migração: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_migrations()

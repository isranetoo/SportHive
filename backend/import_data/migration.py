"""
Script para migrar o banco de dados existente para o novo esquema
sem perder os dados existentes
"""

import os
import sys
import json
import csv
from datetime import datetime

# Adicionar o diretório do backend ao path do Python
# Esta linha deve vir antes de qualquer import relativo ao projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Agora podemos importar módulos do diretório pai
from sqlalchemy import create_engine, text, Column, Integer, String, Float, MetaData, Table
from database import engine

def table_has_column(table_name, column_name):
    """
    Verifica se uma coluna existe em uma tabela no banco de dados.
    
    Args:
        table_name: Nome da tabela
        column_name: Nome da coluna
    
    Returns:
        bool: True se a coluna existir, False caso contrário
    """
    with engine.connect() as conn:
        query = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = :table_name AND column_name = :column_name
        """)
        result = conn.execute(query, {"table_name": table_name, "column_name": column_name})
        return result.fetchone() is not None

def run_migrations():
    """
    Executa as migrações necessárias para atualizar o banco de dados
    sem perder os dados existentes
    """
    print("Iniciando migração do banco de dados...")
    
    # Conectar ao banco de dados
    with engine.connect() as conn:
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
                    if not table_has_column("player_tournament", column["name"]):
                        conn.execute(text(
                            f"ALTER TABLE player_tournament ADD COLUMN {column['name']} {column['type']} DEFAULT {column['default']}"
                        ))
                        print(f"Coluna {column['name']} adicionada à tabela player_tournament.")
                    else:
                        print(f"Coluna {column['name']} já existe na tabela player_tournament.")
            
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

            # Adicionar novas colunas à tabela players
            new_player_columns = [
                {"name": "ranking", "type": "INTEGER", "default": None},
                {"name": "country", "type": "VARCHAR", "default": None},
                {"name": "titles", "type": "INTEGER", "default": 0},
                {"name": "grand_slams", "type": "INTEGER", "default": 0},
                {"name": "hand", "type": "VARCHAR", "default": None},
                {"name": "img_url", "type": "VARCHAR", "default": None},
            ]
            for column in new_player_columns:
                if not table_has_column("players", column["name"]):
                    # Handle NULL defaults by omitting DEFAULT clause
                    if column["default"] is None:
                        conn.execute(text(
                            f"ALTER TABLE players ADD COLUMN {column['name']} {column['type']}"
                        ))
                    else:
                        conn.execute(text(
                            f"ALTER TABLE players ADD COLUMN {column['name']} {column['type']} DEFAULT {column['default']}"
                        ))
                    print(f"Coluna {column['name']} adicionada à tabela players.")
                else:
                    print(f"Coluna {column['name']} já existe na tabela players.")

            # Adicionar novas colunas à tabela tournaments
            new_tournament_columns = [
                {"name": "location", "type": "VARCHAR", "default": None},
                {"name": "date", "type": "VARCHAR", "default": None},
                {"name": "prize", "type": "VARCHAR", "default": None},
                {"name": "img_url", "type": "VARCHAR", "default": None},
            ]
            for column in new_tournament_columns:
                if not table_has_column("tournaments", column["name"]):
                    # Handle NULL defaults by omitting DEFAULT clause
                    if column["default"] is None:
                        conn.execute(text(
                            f"ALTER TABLE tournaments ADD COLUMN {column['name']} {column['type']}"
                        ))
                    else:
                        conn.execute(text(
                            f"ALTER TABLE tournaments ADD COLUMN {column['name']} {column['type']} DEFAULT {column['default']}"
                        ))
                    print(f"Coluna {column['name']} adicionada à tabela tournaments.")
                else:
                    print(f"Coluna {column['name']} já existe na tabela tournaments.")
            
            conn.commit()
            print("Migração concluída com sucesso!")
            
        except Exception as e:
            conn.rollback()
            print(f"Erro durante a migração: {e}")

def import_data(sports_json_path=None, tennis_csv_path=None):
    """
    Importa dados de arquivos JSON e CSV para o banco de dados,
    verificando se já existem para evitar duplicações.
    
    Args:
        sports_json_path: Caminho para o arquivo JSON com dados de esportes
        tennis_csv_path: Caminho para o arquivo CSV com dados de tênis
    """
    from sqlalchemy.orm import Session
    from database import SessionLocal
    from models import Sport, Tournament, Player, TennisMatch, PlayerElo
    
    print("Iniciando importação de dados...")
    
    # Conectar ao banco de dados
    db = SessionLocal()
    
    try:
        # Importar dados de esportes do arquivo JSON
        if sports_json_path and os.path.exists(sports_json_path):
            print(f"Importando dados de esportes de {sports_json_path}...")
            
            # Carregar dados do arquivo JSON
            with open(sports_json_path, 'r', encoding='utf-8') as file:
                sports_data = json.load(file)
            
            # Obter esportes existentes para verificar duplicações
            existing_sports = {sport.name.lower(): sport for sport in db.query(Sport).all()}
            
            inserted_count = 0
            updated_count = 0
            skipped_count = 0
            
            for sport in sports_data:
                sport_name = sport["name"]
                sport_description = sport.get("description", "")
                sport_image = sport.get("image", "")
                sport_category = sport.get("category", "Não categorizado")
                
                # Verificar se o esporte já existe (case-insensitive)
                if sport_name.lower() in existing_sports:
                    existing_sport = existing_sports[sport_name.lower()]
                    # Atualizar campos se necessário
                    updated = False
                    
                    if existing_sport.description != sport_description and sport_description:
                        existing_sport.description = sport_description
                        updated = True
                    
                    if existing_sport.image != sport_image and sport_image:
                        existing_sport.image = sport_image
                        updated = True
                        
                    if hasattr(existing_sport, 'category') and existing_sport.category != sport_category and sport_category:
                        existing_sport.category = sport_category
                        updated = True
                    
                    if updated:
                        print(f"Atualizando: {sport_name}")
                        updated_count += 1
                    else:
                        print(f"Pulando: {sport_name} - Já existe e está atualizado")
                        skipped_count += 1
                else:
                    print(f"Importando: {sport_name}")
                    db.add(Sport(
                        name=sport_name,
                        description=sport_description,
                        image=sport_image,
                        category=sport_category
                    ))
                    inserted_count += 1
            
            print(f"\nResumo da importação de esportes:")
            print(f"✅ {inserted_count} esportes novos importados")
            print(f"🔄 {updated_count} esportes atualizados")
            print(f"⏩ {skipped_count} esportes pulados (já existiam e estavam atualizados)")
        
        # Importar dados de tênis do arquivo CSV
        if tennis_csv_path and os.path.exists(tennis_csv_path):
            print(f"\nImportando dados de tênis de {tennis_csv_path}...")
            
            # Dicionários para armazenar objetos já criados para referência
            tournaments = {}
            players = {}
            
            # Mapear partidas já existentes para evitar duplicação
            existing_matches = {}
            for match in db.query(TennisMatch).all():
                key = (match.tournament_id, match.player1_id, match.player2_id, 
                       match.round, str(match.date))
                existing_matches[key] = match
            
            # Ler o arquivo CSV
            with open(tennis_csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                inserted_matches = 0
                updated_matches = 0
                skipped_matches = 0
                inserted_players = 0
                inserted_tournaments = 0
                
                # Processar cada linha do CSV
                for row in csv_reader:
                    # Processar o torneio
                    tournament_name = row['Tournament']
                    if tournament_name not in tournaments:
                        # Verificar se o torneio já existe no banco de dados
                        tournament = db.query(Tournament).filter(Tournament.name == tournament_name).first()
                        if not tournament:
                            tournament = Tournament(
                                name=tournament_name,
                                series=row['Series'],
                                court=row['Court'],
                                surface=row['Surface']
                            )
                            db.add(tournament)
                            db.flush()  # Para obter o ID gerado
                            inserted_tournaments += 1
                        tournaments[tournament_name] = tournament
                    else:
                        tournament = tournaments[tournament_name]
                    
                    # Processar jogador 1
                    player1_name = row['Player_1']
                    if player1_name not in players:
                        # Verificar se o jogador já existe no banco
                        player1 = db.query(Player).filter(Player.name == player1_name).first()
                        if not player1:
                            player1 = Player(name=player1_name)
                            db.add(player1)
                            db.flush()
                            
                            # Criar o registro ELO para o jogador
                            player_elo = PlayerElo(player_id=player1.id)
                            db.add(player_elo)
                            
                            inserted_players += 1
                        players[player1_name] = player1
                    else:
                        player1 = players[player1_name]
                    
                    # Processar jogador 2
                    player2_name = row['Player_2']
                    if player2_name not in players:
                        # Verificar se o jogador já existe no banco
                        player2 = db.query(Player).filter(Player.name == player2_name).first()
                        if not player2:
                            player2 = Player(name=player2_name)
                            db.add(player2)
                            db.flush()
                            
                            # Criar o registro ELO para o jogador
                            player_elo = PlayerElo(player_id=player2.id)
                            db.add(player_elo)
                            
                            inserted_players += 1
                        players[player2_name] = player2
                    else:
                        player2 = players[player2_name]
                    
                    # Processar vencedor
                    winner_name = row['Winner']
                    if winner_name not in players:
                        # Verificar se o jogador já existe no banco
                        winner = db.query(Player).filter(Player.name == winner_name).first()
                        if not winner:
                            winner = Player(name=winner_name)
                            db.add(winner)
                            db.flush()
                            
                            # Criar o registro ELO para o jogador
                            player_elo = PlayerElo(player_id=winner.id)
                            db.add(player_elo)
                            
                            inserted_players += 1
                        players[winner_name] = winner
                    else:
                        winner = players[winner_name]
                    
                    # Adicionar os jogadores ao torneio se ainda não estiverem relacionados
                    if tournament not in player1.tournaments:
                        player1.tournaments.append(tournament)
                    
                    if tournament not in player2.tournaments:
                        player2.tournaments.append(tournament)
                    
                    # Processar a data
                    match_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
                    
                    # Verificar se a partida já existe
                    match_key = (tournament.id, player1.id, player2.id, row['Round'], str(match_date))
                    if match_key in existing_matches:
                        # A partida já existe, podemos atualizá-la se necessário
                        existing_match = existing_matches[match_key]
                        updated = False
                        
                        # Atualizar informações se necessário
                        if existing_match.winner_id != winner.id:
                            existing_match.winner_id = winner.id
                            updated = True
                        
                        score = row['Score']
                        if existing_match.score != score:
                            existing_match.score = score
                            updated = True
                        
                        if updated:
                            updated_matches += 1
                            if updated_matches % 10 == 0:  # Mostrar apenas a cada 10 para não poluir o console
                                print(f"Atualizando partida: {player1_name} vs {player2_name} ({match_date})")
                        else:
                            skipped_matches += 1
                    else:
                        # Criar nova partida
                        match = TennisMatch(
                            tournament_id=tournament.id,
                            date=match_date,
                            round=row['Round'],
                            best_of=int(row['Best of']),
                            player1_id=player1.id,
                            player2_id=player2.id,
                            winner_id=winner.id,
                            rank1=int(row['Rank_1']) if row['Rank_1'] != '-1' else None,
                            rank2=int(row['Rank_2']) if row['Rank_2'] != '-1' else None,
                            pts1=int(row['Pts_1']) if row['Pts_1'] != '-1' else None,
                            pts2=int(row['Pts_2']) if row['Pts_2'] != '-1' else None,
                            odd1=float(row['Odd_1']) if row['Odd_1'] != '-1.0' else None,
                            odd2=float(row['Odd_2']) if row['Odd_2'] != '-1.0' else None,
                            score=row['Score']
                        )
                        db.add(match)
                        inserted_matches += 1
                        if inserted_matches % 10 == 0:  # Mostrar apenas a cada 10 para não poluir o console
                            print(f"Importando partida: {player1_name} vs {player2_name} ({match_date})")
                
                # Atualizar estatísticas relacionadas
                if inserted_matches > 0 or updated_matches > 0:
                    print("Atualizando estatísticas de confrontos diretos e ELO...")
                    # Esta é uma versão simplificada - para atualização completa, 
                    # considere chamar as funções específicas de update_player_tournament_stats
                    # e calculate_initial_elo do módulo import_tennis_data.py
                
                print(f"\nResumo da importação de tênis:")
                print(f"✅ {inserted_tournaments} torneios novos importados")
                print(f"✅ {inserted_players} jogadores novos importados")
                print(f"✅ {inserted_matches} partidas novas importadas")
                print(f"🔄 {updated_matches} partidas atualizadas")
                print(f"⏩ {skipped_matches} partidas puladas (já existiam e estavam atualizadas)")
        
        # Commit todas as alterações no banco de dados
        db.commit()
        print("\nImportação de dados concluída com sucesso!")
    
    except Exception as e:
        db.rollback()
        print(f"Erro durante a importação: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def update_head_to_head_stats(db):
    """
    Atualiza as estatísticas de confrontos diretos (head-to-head) entre jogadores
    com base nas partidas existentes no banco de dados.
    """
    from models import TennisMatch, PlayerVsPlayer, Tournament
    from sqlalchemy import and_, or_, text
    
    print("Atualizando estatísticas de confrontos diretos...")
    
    # Limpar a tabela para evitar duplicações e erros de contagem
    try:
        db.execute(text("DELETE FROM player_vs_player"))
        print("Tabela player_vs_player limpa para recomputar estatísticas.")
    except Exception as e:
        print(f"Aviso: Não foi possível limpar a tabela player_vs_player: {e}")
    
    # Buscar todas as partidas de tênis
    matches = db.query(TennisMatch).join(Tournament).all()
    
    # Contador para acompanhar progresso
    processed_count = 0
    updated_count = 0
    
    # Dicionário para armazenar os registros de h2h em memória
    # e evitar múltiplas consultas ao banco
    h2h_cache = {}
    
    # Para cada partida, atualizar as estatísticas de confronto direto
    for match in matches:
        processed_count += 1
        
        # Garantir que player1_id seja sempre o ID menor para evitar duplicações
        p1_id = min(match.player1_id, match.player2_id)
        p2_id = max(match.player1_id, match.player2_id)
        
        # Pular se os IDs forem iguais (não deveria acontecer)
        if p1_id == p2_id:
            continue
        
        # Criar uma chave para o cache
        cache_key = (p1_id, p2_id)
        
        # Verificar se já temos este h2h em cache
        if cache_key in h2h_cache:
            h2h = h2h_cache[cache_key]
        else:
            # Buscar registro existente ou criar um novo
            h2h = db.query(PlayerVsPlayer).filter(
                and_(
                    PlayerVsPlayer.player1_id == p1_id,
                    PlayerVsPlayer.player2_id == p2_id
                )
            ).first()
            
            if not h2h:
                # Criar um novo registro com todos os campos inicializados
                h2h = PlayerVsPlayer(
                    player1_id=p1_id,
                    player2_id=p2_id,
                    total_matches=0,
                    player1_wins=0,
                    player2_wins=0,
                    hard_court_matches=0,
                    hard_court_player1_wins=0,
                    hard_court_player2_wins=0,
                    clay_court_matches=0,
                    clay_court_player1_wins=0,
                    clay_court_player2_wins=0,
                    grass_court_matches=0,
                    grass_court_player1_wins=0,
                    grass_court_player2_wins=0,
                    carpet_court_matches=0,
                    carpet_court_player1_wins=0,
                    carpet_court_player2_wins=0,
                    indoor_matches=0,
                    indoor_player1_wins=0,
                    indoor_player2_wins=0,
                    outdoor_matches=0,
                    outdoor_player1_wins=0,
                    outdoor_player2_wins=0
                )
                db.add(h2h)
                updated_count += 1
            
            # Adicionar ao cache
            h2h_cache[cache_key] = h2h
        
        # Determinar quem ganhou a partida
        if match.winner_id == p1_id:
            # Player 1 ganhou
            player1_won = True
        elif match.winner_id == p2_id:
            # Player 2 ganhou
            player1_won = False
        else:
            # Isso não deveria acontecer, pular esta partida
            continue
        
        # Garantir que os contadores não sejam None antes de incrementar
        if h2h.total_matches is None:
            h2h.total_matches = 0
        h2h.total_matches += 1
        
        if player1_won:
            if h2h.player1_wins is None:
                h2h.player1_wins = 0
            h2h.player1_wins += 1
        else:
            if h2h.player2_wins is None:
                h2h.player2_wins = 0
            h2h.player2_wins += 1
        
        # Atualizar estatísticas por superfície
        court_type = match.tournament.surface.lower() if match.tournament.surface else "unknown"
        indoor_outdoor = match.tournament.court.lower() if match.tournament.court else "unknown"
        
        # Quadra dura
        if "hard" in court_type:
            if h2h.hard_court_matches is None:
                h2h.hard_court_matches = 0
            h2h.hard_court_matches += 1
            
            if player1_won:
                if h2h.hard_court_player1_wins is None:
                    h2h.hard_court_player1_wins = 0
                h2h.hard_court_player1_wins += 1
            else:
                if h2h.hard_court_player2_wins is None:
                    h2h.hard_court_player2_wins = 0
                h2h.hard_court_player2_wins += 1
        
        # Saibro
        elif "clay" in court_type:
            if h2h.clay_court_matches is None:
                h2h.clay_court_matches = 0
            h2h.clay_court_matches += 1
            
            if player1_won:
                if h2h.clay_court_player1_wins is None:
                    h2h.clay_court_player1_wins = 0
                h2h.clay_court_player1_wins += 1
            else:
                if h2h.clay_court_player2_wins is None:
                    h2h.clay_court_player2_wins = 0
                h2h.clay_court_player2_wins += 1
        
        # Grama
        elif "grass" in court_type:
            if h2h.grass_court_matches is None:
                h2h.grass_court_matches = 0
            h2h.grass_court_matches += 1
            
            if player1_won:
                if h2h.grass_court_player1_wins is None:
                    h2h.grass_court_player1_wins = 0
                h2h.grass_court_player1_wins += 1
            else:
                if h2h.grass_court_player2_wins is None:
                    h2h.grass_court_player2_wins = 0
                h2h.grass_court_player2_wins += 1
        
        # Carpete
        elif "carpet" in court_type:
            if h2h.carpet_court_matches is None:
                h2h.carpet_court_matches = 0
            h2h.carpet_court_matches += 1
            
            if player1_won:
                if h2h.carpet_court_player1_wins is None:
                    h2h.carpet_court_player1_wins = 0
                h2h.carpet_court_player1_wins += 1
            else:
                if h2h.carpet_court_player2_wins is None:
                    h2h.carpet_court_player2_wins = 0
                h2h.carpet_court_player2_wins += 1
        
        # Indoor/Outdoor
        if "indoor" in indoor_outdoor:
            if h2h.indoor_matches is None:
                h2h.indoor_matches = 0
            h2h.indoor_matches += 1
            
            if player1_won:
                if h2h.indoor_player1_wins is None:
                    h2h.indoor_player1_wins = 0
                h2h.indoor_player1_wins += 1
            else:
                if h2h.indoor_player2_wins is None:
                    h2h.indoor_player2_wins = 0
                h2h.indoor_player2_wins += 1
                
        elif "outdoor" in indoor_outdoor:
            if h2h.outdoor_matches is None:
                h2h.outdoor_matches = 0
            h2h.outdoor_matches += 1
            
            if player1_won:
                if h2h.outdoor_player1_wins is None:
                    h2h.outdoor_player1_wins = 0
                h2h.outdoor_player1_wins += 1
            else:
                if h2h.outdoor_player2_wins is None:
                    h2h.outdoor_player2_wins = 0
                h2h.outdoor_player2_wins += 1
        
        # Mostrar progresso a cada 100 partidas
        if processed_count % 100 == 0:
            print(f"Processadas {processed_count} partidas...")
    
    # Realizar commit periódico para evitar transações muito grandes
    db.commit()
    print(f"Estatísticas de confrontos diretos atualizadas: {updated_count} novos registros criados.")
    return processed_count

def update_statistics():
    """
    Atualiza estatísticas após importação de dados
    """
    try:
        # Verificar se o arquivo import_tennis_data.py existe no mesmo diretório
        import_tennis_data_path = os.path.join(os.path.dirname(__file__), "import_tennis_data.py")
        if not os.path.exists(import_tennis_data_path):
            print(f"AVISO: Arquivo import_tennis_data.py não encontrado em {os.path.dirname(__file__)}")
            print("Por favor, certifique-se de que o arquivo existe em um destes locais:")
            print(f"  - {os.path.join(os.path.dirname(__file__), 'import_tennis_data.py')}")
            print(f"  - {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'import_tennis_data.py')}")
            return
            
        # Importando aqui para evitar dependências circulares
        try:
            # Tentar importar do pacote import_data
            from .import_tennis_data import update_player_tournament_stats, calculate_initial_elo
        except ImportError:
            # Tentar importar como módulo no mesmo nível
            from import_tennis_data import update_player_tournament_stats, calculate_initial_elo
            
        from database import SessionLocal
        
        db = SessionLocal()
        try:
            print("Atualizando estatísticas das partidas...")
            update_player_tournament_stats(db)
            
            # Adicionar chamada para atualizar os confrontos diretos
            print("Atualizando estatísticas de confrontos diretos...")
            update_head_to_head_stats(db)
            
            print("Calculando rankings ELO iniciais...")
            calculate_initial_elo(db)
            db.commit()
            print("✅ Estatísticas atualizadas com sucesso!")
        except Exception as e:
            db.rollback()
            print(f"Erro ao atualizar estatísticas: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
    except ImportError as e:
        print(f"Não foi possível importar funções de estatísticas: {e}")
        print("\nPara resolver este problema:")
        print("1. Verifique se o arquivo import_tennis_data.py existe no diretório import_data")
        print("2. Certifique-se de que o arquivo contém as funções update_player_tournament_stats e calculate_initial_elo")
        print("3. Se o arquivo não existir, você pode criar um arquivo vazio ou copiar as funções de outro lugar")
        
        # Tentar executar apenas o update de confrontos diretos
        print("\nTentando atualizar apenas as estatísticas de confrontos diretos...")
        try:
            from database import SessionLocal
            db = SessionLocal()
            try:
                updated = update_head_to_head_stats(db)
                db.commit()
                print(f"✅ Atualização de confrontos diretos concluída com sucesso! ({updated} partidas processadas)")
            except Exception as e:
                db.rollback()
                print(f"Erro ao atualizar confrontos diretos: {e}")
                import traceback
                traceback.print_exc()
            finally:
                db.close()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

if __name__ == "__main__":
    import argparse
    
    # Define default file paths
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    default_sports_path = os.path.join(data_dir, "sports.json")
    
    # Verificar qual arquivo de tênis existe
    default_tennis_path = os.path.join(data_dir, "tennis.csv")
    atp_tennis_path = os.path.join(data_dir, "atp_tennis.csv")
    
    if not os.path.exists(default_tennis_path) and os.path.exists(atp_tennis_path):
        default_tennis_path = atp_tennis_path
    
    parser = argparse.ArgumentParser(description="Migra o banco de dados e importa dados")
    parser.add_argument("--run-migrations", action="store_true", 
                        help="Executa as migrações de esquema do banco de dados")
    parser.add_argument("--import-sports", metavar="FILE", 
                        help=f"Importa dados de esportes do arquivo JSON especificado")
    parser.add_argument("--import-tennis", metavar="FILE", 
                        help=f"Importa dados de tênis do arquivo CSV especificado")
    parser.add_argument("--update-stats", action="store_true",
                        help="Atualiza estatísticas após importação")
    # Novos argumentos simplificados
    parser.add_argument("--all", action="store_true",
                        help="Executa migrações, importa todos os dados e atualiza estatísticas")
    parser.add_argument("--sports", action="store_true",
                        help=f"Importa apenas dados de esportes do arquivo padrão")
    parser.add_argument("--tennis", action="store_true",
                        help=f"Importa apenas dados de tênis do arquivo padrão")
    
    args = parser.parse_args()
    
    # Processar os novos argumentos simplificados
    if args.all:
        print(f"Iniciando importação completa com arquivos padrão...")
        
        if not os.path.exists(default_sports_path):
            print(f"AVISO: Arquivo de esportes não encontrado em {default_sports_path}")
        
        if not os.path.exists(default_tennis_path):
            print(f"AVISO: Arquivo de tênis não encontrado. Tentei buscar:")
            print(f"  - {os.path.join(data_dir, 'tennis.csv')}")
            print(f"  - {os.path.join(data_dir, 'atp_tennis.csv')}")
            print("Por favor, verifique se o arquivo existe nestes caminhos.")
        else:
            print(f"Usando arquivo de tênis: {default_tennis_path}")
        
        run_migrations()
        import_data(
            sports_json_path=default_sports_path,
            tennis_csv_path=default_tennis_path
        )
        update_statistics()
        sys.exit(0)
    
    if args.sports:
        print(f"Importando apenas dados de esportes do arquivo padrão: {default_sports_path}")
        import_data(sports_json_path=default_sports_path)
        sys.exit(0)
    
    if args.tennis:
        print(f"Importando apenas dados de tênis do arquivo padrão: {default_tennis_path}")
        if not os.path.exists(default_tennis_path):
            print(f"ERRO: Arquivo de tênis não encontrado em {default_tennis_path}")
            print("Tentei buscar também em:", atp_tennis_path)
            print("Por favor, use --import-tennis para especificar o caminho correto.")
            sys.exit(1)
        import_data(tennis_csv_path=default_tennis_path)
        sys.exit(0)
    
    # Processar os argumentos originais
    if args.run_migrations:
        run_migrations()
    
    if args.import_sports or args.import_tennis:
        import_data(
            sports_json_path=args.import_sports,
            tennis_csv_path=args.import_tennis
        )
        
    if args.update_stats:
        update_statistics()

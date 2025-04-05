import csv
import datetime
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, init_db, recreate_db, table_has_column, engine
from models import Tournament, Player, TennisMatch, player_tournament, PlayerVsPlayer, PlayerElo
from sqlalchemy import select, func, or_, and_, text

def check_schema_compatibility():
    """
    Verifica se o esquema do banco de dados é compatível com os modelos atuais.
    Retorna True se o esquema estiver atualizado, False caso contrário.
    """
    db = SessionLocal()
    try:
        # Verificar se as tabelas necessárias existem
        required_tables = ["player_tournament", "player_vs_player", "player_elo"]
        for table in required_tables:
            try:
                db.execute(text(f"SELECT 1 FROM {table} LIMIT 1"))
            except Exception:
                print(f"Tabela {table} não existe ou está incompleta.")
                return False
        
        # Verificar se as colunas necessárias existem na tabela player_tournament
        required_columns = [
            "losses", "hard_court_wins", "clay_court_wins", 
            "grass_court_wins", "carpet_court_wins", "indoor_wins", 
            "outdoor_wins", "elo_rating"
        ]
        
        for column in required_columns:
            if not table_has_column("player_tournament", column):
                print(f"Coluna {column} não existe na tabela player_tournament.")
                return False
        
        return True
    except Exception as e:
        print(f"Erro ao verificar esquema: {e}")
        return False
    finally:
        db.close()

def import_tennis_data(csv_file_path, force_recreate=False):
    """
    Importa dados de tênis do arquivo CSV para o banco de dados
    
    Args:
        csv_file_path: Caminho para o arquivo CSV
        force_recreate: Se True, recria as tabelas do banco de dados
    """
    # Verificar compatibilidade do esquema
    if force_recreate or not check_schema_compatibility():
        print("Recriando tabelas do banco de dados...")
        try:
            recreate_db()
        except Exception as e:
            print(f"Erro ao recriar banco de dados: {e}")
            print("Tentando abordagem alternativa...")
            # Manual alternative approach for PostgreSQL
            if not os.getenv("USE_SQLITE", "False").lower() in ("true", "1", "t"):
                conn = engine.raw_connection()
                try:
                    with conn.cursor() as cur:
                        # Drop tables with foreign keys first
                        cur.execute("DROP TABLE IF EXISTS tennis_matches CASCADE;")
                        cur.execute("DROP TABLE IF EXISTS player_tournament CASCADE;")
                        cur.execute("DROP TABLE IF EXISTS player_elo CASCADE;")
                        cur.execute("DROP TABLE IF EXISTS player_vs_player CASCADE;")
                        # Drop main tables
                        cur.execute("DROP TABLE IF EXISTS players CASCADE;")
                        cur.execute("DROP TABLE IF EXISTS tournaments CASCADE;")
                        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
                        cur.execute("DROP TABLE IF EXISTS sports CASCADE;")
                        
                        # Drop sequences
                        cur.execute("DROP SEQUENCE IF EXISTS players_id_seq CASCADE;")
                        cur.execute("DROP SEQUENCE IF EXISTS tournaments_id_seq CASCADE;")
                        cur.execute("DROP SEQUENCE IF EXISTS tennis_matches_id_seq CASCADE;")
                        cur.execute("DROP SEQUENCE IF EXISTS player_vs_player_id_seq CASCADE;")
                        cur.execute("DROP SEQUENCE IF EXISTS player_elo_id_seq CASCADE;")
                        cur.execute("DROP SEQUENCE IF EXISTS users_id_seq CASCADE;")
                        cur.execute("DROP SEQUENCE IF EXISTS sports_id_seq CASCADE;")
                    conn.commit()
                    print("Tabelas e sequências removidas manualmente.")
                except Exception as e:
                    conn.rollback()
                    print(f"Erro na limpeza manual do banco: {e}")
                finally:
                    conn.close()
            
            # Now try to initialize again
            init_db()
    else:
        print("Esquema de banco de dados compatível, continuando com a importação...")
    
    # Inicializa a sessão do banco de dados
    db = SessionLocal()
    
    # Dicionários para armazenar objetos já criados para referência
    tournaments = {}
    players = {}
    
    try:
        # Abre o arquivo CSV
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Processa cada linha do CSV
            for row in csv_reader:
                # Processa o torneio
                tournament_name = row['Tournament']
                if tournament_name not in tournaments:
                    tournament = Tournament(
                        name=tournament_name,
                        series=row['Series'],
                        court=row['Court'],
                        surface=row['Surface']
                    )
                    db.add(tournament)
                    db.flush()  # Para obter o ID gerado
                    tournaments[tournament_name] = tournament
                else:
                    tournament = tournaments[tournament_name]
                
                # Processa jogador 1
                player1_name = row['Player_1']
                if player1_name not in players:
                    player1 = Player(name=player1_name)
                    db.add(player1)
                    db.flush()
                    
                    # Cria o registro ELO para o jogador
                    player_elo = PlayerElo(player_id=player1.id)
                    db.add(player_elo)
                    
                    players[player1_name] = player1
                else:
                    player1 = players[player1_name]
                
                # Processa jogador 2
                player2_name = row['Player_2']
                if player2_name not in players:
                    player2 = Player(name=player2_name)
                    db.add(player2)
                    db.flush()
                    
                    # Cria o registro ELO para o jogador
                    player_elo = PlayerElo(player_id=player2.id)
                    db.add(player_elo)
                    
                    players[player2_name] = player2
                else:
                    player2 = players[player2_name]
                
                # Processa vencedor
                winner_name = row['Winner']
                if winner_name not in players:
                    winner = Player(name=winner_name)
                    db.add(winner)
                    db.flush()
                    
                    # Cria o registro ELO para o jogador
                    player_elo = PlayerElo(player_id=winner.id)
                    db.add(player_elo)
                    
                    players[winner_name] = winner
                else:
                    winner = players[winner_name]
                
                # Adiciona os jogadores ao torneio se ainda não estiverem relacionados
                if tournament not in player1.tournaments:
                    player1.tournaments.append(tournament)
                
                if tournament not in player2.tournaments:
                    player2.tournaments.append(tournament)
                
                # Processa a data
                match_date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d').date()
                
                # Cria o objeto TennisMatch
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
                db.flush()  # Para obter o ID
                
                # Atualiza o histórico de confrontos diretos
                update_head_to_head(db, match, tournament)
            
            # Commit todas as alterações no banco de dados
            db.commit()
            
            # Após importar todos os dados, vamos atualizar as estatísticas
            update_player_tournament_stats(db)
            calculate_initial_elo(db)
            
            print(f"Importação concluída com sucesso!")
            
    except Exception as e:
        db.rollback()
        print(f"Erro durante a importação: {e}")
    finally:
        db.close()

def update_head_to_head(db, match, tournament):
    """
    Atualiza ou cria um registro de confronto direto entre dois jogadores
    """
    # Vamos sempre ordenar os IDs para garantir consistência
    player1_id = min(match.player1_id, match.player2_id)
    player2_id = max(match.player2_id, match.player1_id)
    
    # Busca o registro existente ou cria um novo
    h2h = db.query(PlayerVsPlayer).filter(
        PlayerVsPlayer.player1_id == player1_id,
        PlayerVsPlayer.player2_id == player2_id
    ).first()
    
    if not h2h:
        h2h = PlayerVsPlayer(
            player1_id=player1_id,
            player2_id=player2_id,
            total_matches=0,
            player1_wins=0,
            player2_wins=0,
            # Inicializar todos os contadores específicos de superfície
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
    
    # Incrementa o total de partidas
    h2h.total_matches += 1
    
    # Determina quem ganhou
    if match.winner_id == player1_id:
        h2h.player1_wins += 1
    else:
        h2h.player2_wins += 1
    
    # Atualiza estatísticas por superfície
    surface = tournament.surface.lower() if tournament.surface else "unknown"
    court_type = tournament.court.lower() if tournament.court else "unknown"
    
    if "hard" in surface:
        h2h.hard_court_matches += 1
        if match.winner_id == player1_id:
            h2h.hard_court_player1_wins += 1
        else:
            h2h.hard_court_player2_wins += 1
    elif "clay" in surface:
        h2h.clay_court_matches += 1
        if match.winner_id == player1_id:
            h2h.clay_court_player1_wins += 1
        else:
            h2h.clay_court_player2_wins += 1
    elif "grass" in surface:
        h2h.grass_court_matches += 1
        if match.winner_id == player1_id:
            h2h.grass_court_player1_wins += 1
        else:
            h2h.grass_court_player2_wins += 1
    elif "carpet" in surface:
        h2h.carpet_court_matches += 1
        if match.winner_id == player1_id:
            h2h.carpet_court_player1_wins += 1
        else:
            h2h.carpet_court_player2_wins += 1
    
    # Indoor/Outdoor
    if "indoor" in court_type:
        h2h.indoor_matches += 1
        if match.winner_id == player1_id:
            h2h.indoor_player1_wins += 1
        else:
            h2h.indoor_player2_wins += 1
    elif "outdoor" in court_type:
        h2h.outdoor_matches += 1
        if match.winner_id == player1_id:
            h2h.outdoor_player1_wins += 1
        else:
            h2h.outdoor_player2_wins += 1

def update_player_tournament_stats(db):
    """
    Atualiza as estatísticas da tabela player_tournament com base nas partidas
    """
    # Consulta para obter todas as partidas
    matches = db.query(TennisMatch).join(Tournament).all()
    
    stats = {}  # Dicionário para armazenar estatísticas
    
    for match in matches:
        # Chaves para identificar o par jogador-torneio
        player1_key = (match.player1_id, match.tournament_id)
        player2_key = (match.player2_id, match.tournament_id)
        
        # Inicializa as estatísticas para o jogador 1 se ainda não existirem
        if player1_key not in stats:
            stats[player1_key] = {
                'appearances': 0, 'wins': 0, 'losses': 0,
                'hard_court_wins': 0, 'clay_court_wins': 0, 
                'grass_court_wins': 0, 'carpet_court_wins': 0,
                'indoor_wins': 0, 'outdoor_wins': 0
            }
        
        # Inicializa as estatísticas para o jogador 2 se ainda não existirem
        if player2_key not in stats:
            stats[player2_key] = {
                'appearances': 0, 'wins': 0, 'losses': 0,
                'hard_court_wins': 0, 'clay_court_wins': 0, 
                'grass_court_wins': 0, 'carpet_court_wins': 0,
                'indoor_wins': 0, 'outdoor_wins': 0
            }
        
        # Incrementa as aparições
        stats[player1_key]['appearances'] += 1
        stats[player2_key]['appearances'] += 1
        
        # Atualiza vitórias/derrotas
        if match.winner_id == match.player1_id:
            stats[player1_key]['wins'] += 1
            stats[player2_key]['losses'] += 1
            
            # Atualiza estatísticas por superfície para o vencedor
            surface = match.tournament.surface.lower() if match.tournament.surface else "unknown"
            court_type = match.tournament.court.lower() if match.tournament.court else "unknown"
            
            if "hard" in surface:
                stats[player1_key]['hard_court_wins'] += 1
            elif "clay" in surface:
                stats[player1_key]['clay_court_wins'] += 1
            elif "grass" in surface:
                stats[player1_key]['grass_court_wins'] += 1
            elif "carpet" in surface:
                stats[player1_key]['carpet_court_wins'] += 1
            
            if "indoor" in court_type:
                stats[player1_key]['indoor_wins'] += 1
            elif "outdoor" in court_type:
                stats[player1_key]['outdoor_wins'] += 1
                
        else:
            stats[player2_key]['wins'] += 1
            stats[player1_key]['losses'] += 1
            
            # Atualiza estatísticas por superfície para o vencedor
            surface = match.tournament.surface.lower() if match.tournament.surface else "unknown"
            court_type = match.tournament.court.lower() if match.tournament.court else "unknown"
            
            if "hard" in surface:
                stats[player2_key]['hard_court_wins'] += 1
            elif "clay" in surface:
                stats[player2_key]['clay_court_wins'] += 1
            elif "grass" in surface:
                stats[player2_key]['grass_court_wins'] += 1
            elif "carpet" in surface:
                stats[player2_key]['carpet_court_wins'] += 1
            
            if "indoor" in court_type:
                stats[player2_key]['indoor_wins'] += 1
            elif "outdoor" in court_type:
                stats[player2_key]['outdoor_wins'] += 1
    
    # Atualiza a tabela player_tournament com as estatísticas coletadas
    for (player_id, tournament_id), stat in stats.items():
        stmt = player_tournament.update().where(
            (player_tournament.c.player_id == player_id) & 
            (player_tournament.c.tournament_id == tournament_id)
        ).values(**stat)
        db.execute(stmt)
    
    db.commit()

def calculate_initial_elo(db):
    """
    Calcula os ratings ELO iniciais para todos os jogadores
    """
    # Implementação básica de ELO - pode ser expandida no futuro
    # Para cada jogador, baseia-se na taxa de vitórias
    players = db.query(Player).all()
    for player in players:
        total_matches = len(player.matches_as_player1) + len(player.matches_as_player2)
        if total_matches == 0:
            continue
        
        wins = len([m for m in player.matches_as_player1 if m.winner_id == player.id]) + \
               len([m for m in player.matches_as_player2 if m.winner_id == player.id])
        
        win_rate = wins / total_matches
        
        # Calcular ELO básico (entre 1400 e 2000)
        base_elo = 1500 + (win_rate * 500)
        
        # Atualizar o registro de ELO do jogador
        elo_record = db.query(PlayerElo).filter(PlayerElo.player_id == player.id).first()
        if elo_record:
            elo_record.elo_rating = base_elo
            elo_record.last_updated = datetime.datetime.now().date()
        
        # Calcular ELO por superfície
        surfaces = {
            'hard': {'matches': 0, 'wins': 0},
            'clay': {'matches': 0, 'wins': 0},
            'grass': {'matches': 0, 'wins': 0},
            'carpet': {'matches': 0, 'wins': 0}
        }
        
        court_types = {
            'indoor': {'matches': 0, 'wins': 0},
            'outdoor': {'matches': 0, 'wins': 0}
        }
        
        # Coletar dados por superfície e tipo de quadra
        for match in player.matches_as_player1 + player.matches_as_player2:
            tournament = db.query(Tournament).filter(Tournament.id == match.tournament_id).first()
            if not tournament:
                continue
                
            surface = tournament.surface.lower() if tournament.surface else "unknown"
            court_type = tournament.court.lower() if tournament.court else "unknown"
            
            is_winner = match.winner_id == player.id
            
            for key in surfaces:
                if key in surface:
                    surfaces[key]['matches'] += 1
                    if is_winner:
                        surfaces[key]['wins'] += 1
            
            for key in court_types:
                if key in court_type:
                    court_types[key]['matches'] += 1
                    if is_winner:
                        court_types[key]['wins'] += 1
        
        # Calcular ELO por superfície
        if elo_record:
            for surface, data in surfaces.items():
                if data['matches'] > 0:
                    win_rate = data['wins'] / data['matches']
                    surface_elo = 1500 + (win_rate * 500)
                    
                    if surface == 'hard':
                        elo_record.hard_court_elo = surface_elo
                    elif surface == 'clay':
                        elo_record.clay_court_elo = surface_elo
                    elif surface == 'grass':
                        elo_record.grass_court_elo = surface_elo
                    elif surface == 'carpet':
                        elo_record.carpet_court_elo = surface_elo
            
            # Calcular ELO por tipo de quadra
            for court_type, data in court_types.items():
                if data['matches'] > 0:
                    win_rate = data['wins'] / data['matches']
                    court_elo = 1500 + (win_rate * 500)
                    
                    if court_type == 'indoor':
                        elo_record.indoor_elo = court_elo
                    elif court_type == 'outdoor':
                        elo_record.outdoor_elo = court_elo
    
    db.commit()

if __name__ == "__main__":
    init_db()  # Certifica-se de que as tabelas foram criadas
    import_tennis_data("c:\\Users\\Israel Neto\\Desktop\\SportHive\\backend\\import_data\\atp_tennis.csv", force_recreate=True)

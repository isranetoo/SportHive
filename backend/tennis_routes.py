from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Tournament, Player, TennisMatch, player_tournament, PlayerVsPlayer, PlayerElo
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from sqlalchemy import select, func, or_, and_

router = APIRouter()

class PlayerModel(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class TournamentModel(BaseModel):
    id: int
    name: str
    series: Optional[str]
    court: Optional[str]
    surface: Optional[str]
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class TennisMatchModel(BaseModel):
    id: int
    tournament: TournamentModel
    date: str
    round: str
    player1: PlayerModel
    player2: PlayerModel
    winner: PlayerModel
    score: Optional[str]
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class PlayerTournamentStats(BaseModel):
    player_id: int
    player_name: str
    tournament_id: int
    tournament_name: str
    appearances: int
    wins: int
    best_round: Optional[str]
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class PlayerEloModel(BaseModel):
    player_id: int
    player_name: str
    elo_rating: float
    hard_court_elo: float
    clay_court_elo: float
    grass_court_elo: float
    carpet_court_elo: float
    indoor_elo: float
    outdoor_elo: float
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class DetailedPlayerTournamentStats(BaseModel):
    player_id: int
    player_name: str
    tournament_id: int
    tournament_name: str
    appearances: int
    wins: int
    losses: int
    win_percentage: float
    hard_court_wins: int
    clay_court_wins: int
    grass_court_wins: int
    carpet_court_wins: int
    indoor_wins: int
    outdoor_wins: int
    elo_rating: float
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class HeadToHeadDetailedModel(BaseModel):
    player1: PlayerModel
    player2: PlayerModel
    matchup_description: str  # Added field
    total_matches: int
    player1_wins: int
    player2_wins: int
    hard_court: Dict[str, Any]
    clay_court: Dict[str, Any]
    grass_court: Dict[str, Any]
    carpet_court: Dict[str, Any]
    indoor: Dict[str, Any]
    outdoor: Dict[str, Any]
    tournaments: Dict[str, Any]
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class PlayerTourneyMatchupsModel(BaseModel):
    tournament_id: int
    tournament_name: str
    opponents: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class TournamentMatchupsModel(BaseModel):
    player1_id: int
    player1_name: str
    player2_id: int
    player2_name: str
    matches_count: int
    tournament_id: int
    
    class Config:
        from_attributes = True  # Updated from orm_mode

class TournamentPlayerStatsModel(BaseModel):
    player_id: int
    player_name: str
    wins: int
    losses: int
    win_percentage: float
    tournament_id: int
    tournament_name: str
    
    class Config:
        from_attributes = True  # Updated from orm_mode

@router.get("/api/tennis/players", response_model=List[PlayerModel])
def get_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obter lista de jogadores de tênis"""
    players = db.query(Player).offset(skip).limit(limit).all()
    return players

@router.get("/api/tennis/tournaments", response_model=List[TournamentModel])
def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obter lista de torneios de tênis"""
    tournaments = db.query(Tournament).offset(skip).limit(limit).all()
    return tournaments

@router.get("/api/tennis/matches", response_model=List[TennisMatchModel])
def get_matches(
    tournament_id: Optional[int] = None,
    player_id: Optional[int] = None,
    surface: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Obter partidas de tênis com filtros opcionais"""
    query = db.query(TennisMatch)
    
    if tournament_id:
        query = query.filter(TennisMatch.tournament_id == tournament_id)
    
    if player_id:
        query = query.filter(
            (TennisMatch.player1_id == player_id) | 
            (TennisMatch.player2_id == player_id)
        )
    
    if surface:
        query = query.join(Tournament).filter(Tournament.surface == surface)
    
    matches = query.offset(skip).limit(limit).all()
    return matches

@router.get("/api/tennis/player/{player_id}/tournaments", response_model=List[TournamentModel])
def get_player_tournaments(player_id: int, db: Session = Depends(get_db)):
    """Obter todos os torneios em que um jogador participou"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    return player.tournaments

@router.get("/api/tennis/tournament/{tournament_id}/players", response_model=List[PlayerModel])
def get_tournament_players(tournament_id: int, db: Session = Depends(get_db)):
    """Obter todos os jogadores que participaram de um torneio"""
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneio não encontrado")
    
    return tournament.players

@router.get("/api/tennis/player-tournament-stats", response_model=List[PlayerTournamentStats])
def get_player_tournament_stats(
    player_id: Optional[int] = None,
    tournament_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obter estatísticas de jogadores em torneios.
    Pode filtrar por jogador ou torneio.
    """
    query = select(
        player_tournament.c.player_id,
        Player.name.label("player_name"),
        player_tournament.c.tournament_id,
        Tournament.name.label("tournament_name"),
        player_tournament.c.appearances,
        player_tournament.c.wins,
        player_tournament.c.best_round
    ).select_from(
        player_tournament
    ).join(
        Player, Player.id == player_tournament.c.player_id
    ).join(
        Tournament, Tournament.id == player_tournament.c.tournament_id
    )
    
    if player_id:
        query = query.where(player_tournament.c.player_id == player_id)
    
    if tournament_id:
        query = query.where(player_tournament.c.tournament_id == tournament_id)
    
    results = db.execute(query).all()
    
    return [
        {
            "player_id": result.player_id,
            "player_name": result.player_name,  # Inclui o nome do jogador
            "tournament_id": result.tournament_id,
            "tournament_name": result.tournament_name,
            "appearances": result.appearances,
            "wins": result.wins,
            "best_round": result.best_round
        }
        for result in results
    ]

@router.get("/api/tennis/head-to-head", response_model=Dict[str, Any])
def get_head_to_head(player1_id: int, player2_id: int, db: Session = Depends(get_db)):
    """
    Obter estatísticas de confronto direto entre dois jogadores.
    """
    # Verificar se os jogadores existem
    player1 = db.query(Player).filter(Player.id == player1_id).first()
    player2 = db.query(Player).filter(Player.id == player2_id).first()
    
    if not player1 or not player2:
        raise HTTPException(status_code=404, detail="Um ou ambos os jogadores não encontrados")
    
    # Consulta para encontrar partidas entre os dois jogadores
    query = db.query(TennisMatch).filter(
        ((TennisMatch.player1_id == player1_id) & (TennisMatch.player2_id == player2_id)) |
        ((TennisMatch.player1_id == player2_id) & (TennisMatch.player2_id == player1_id))
    )
    
    matches = query.all()
    
    # Calcular estatísticas
    total_matches = len(matches)
    player1_wins = sum(1 for match in matches if match.winner_id == player1_id)
    player2_wins = sum(1 for match in matches if match.winner_id == player2_id)
    
    # Agrupar partidas por torneio
    matches_by_tournament = {}
    for match in matches:
        if match.tournament.name not in matches_by_tournament:
            matches_by_tournament[match.tournament.name] = {
                "total": 0,
                "player1_wins": 0,
                "player2_wins": 0
            }
        
        matches_by_tournament[match.tournament.name]["total"] += 1
        if match.winner_id == player1_id:
            matches_by_tournament[match.tournament.name]["player1_wins"] += 1
        else:
            matches_by_tournament[match.tournament.name]["player2_wins"] += 1
    
    h2h = db.query(PlayerVsPlayer).filter(
        ((PlayerVsPlayer.player1_id == player1_id) & (PlayerVsPlayer.player2_id == player2_id)) |
        ((PlayerVsPlayer.player1_id == player2_id) & (PlayerVsPlayer.player2_id == player1_id))
    ).first()
    
    if not h2h:
        raise HTTPException(status_code=404, detail="Confronto direto não encontrado")
    
    return {
        "player1": {
            "id": h2h.player1_id,
            "name": h2h.player1_name
        },
        "player2": {
            "id": h2h.player2_id,
            "name": h2h.player2_name
        },
        "total_matches": h2h.total_matches,
        "player1_wins": h2h.player1_wins,
        "player2_wins": h2h.player2_wins,
        "matches_by_tournament": matches_by_tournament
    }

@router.get("/api/tennis/player-tournament-detailed", response_model=List[DetailedPlayerTournamentStats])
def get_detailed_player_tournament_stats(
    player_id: Optional[int] = None,
    tournament_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obter estatísticas detalhadas de jogadores em torneios.
    Pode filtrar por jogador ou torneio.
    """
    query = select(
        player_tournament.c.player_id,
        Player.name.label("player_name"),
        player_tournament.c.tournament_id,
        Tournament.name.label("tournament_name"),
        player_tournament.c.appearances,
        player_tournament.c.wins,
        player_tournament.c.losses,
        player_tournament.c.hard_court_wins,
        player_tournament.c.clay_court_wins,
        player_tournament.c.grass_court_wins,
        player_tournament.c.carpet_court_wins,
        player_tournament.c.indoor_wins,
        player_tournament.c.outdoor_wins,
        player_tournament.c.elo_rating
    ).select_from(
        player_tournament
    ).join(
        Player, Player.id == player_tournament.c.player_id
    ).join(
        Tournament, Tournament.id == player_tournament.c.tournament_id
    )
    
    if player_id:
        query = query.where(player_tournament.c.player_id == player_id)
    
    if tournament_id:
        query = query.where(player_tournament.c.tournament_id == tournament_id)
    
    results = db.execute(query).all()
    
    return [
        {
            "player_id": result.player_id,
            "player_name": result.player_name,
            "tournament_id": result.tournament_id,
            "tournament_name": result.tournament_name,
            "appearances": result.appearances,
            "wins": result.wins,
            "losses": result.losses,
            "win_percentage": (result.wins / result.appearances * 100) if result.appearances > 0 else 0,
            "hard_court_wins": result.hard_court_wins,
            "clay_court_wins": result.clay_court_wins,
            "grass_court_wins": result.grass_court_wins,
            "carpet_court_wins": result.carpet_court_wins,
            "indoor_wins": result.indoor_wins,
            "outdoor_wins": result.outdoor_wins,
            "elo_rating": result.elo_rating
        }
        for result in results
    ]

@router.get("/api/tennis/player/{player_id}/elo", response_model=PlayerEloModel)
def get_player_elo(player_id: int, db: Session = Depends(get_db)):
    """Obter as classificações ELO de um jogador"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    elo = db.query(PlayerElo).filter(PlayerElo.player_id == player_id).first()
    if not elo:
        raise HTTPException(status_code=404, detail="Rating ELO não encontrado para este jogador")
    
    return {
        "player_id": player.id,
        "player_name": player.name,
        "elo_rating": elo.elo_rating,
        "hard_court_elo": elo.hard_court_elo,
        "clay_court_elo": elo.clay_court_elo,
        "grass_court_elo": elo.grass_court_elo,
        "carpet_court_elo": elo.carpet_court_elo,
        "indoor_elo": elo.indoor_elo,
        "outdoor_elo": elo.outdoor_elo
    }

@router.get("/api/tennis/head-to-head-detailed", response_model=HeadToHeadDetailedModel)
def get_detailed_head_to_head(player1_id: int, player2_id: int, db: Session = Depends(get_db)):
    """
    Obter estatísticas detalhadas de confronto direto entre dois jogadores
    """
    # Verificar se os jogadores existem
    player1 = db.query(Player).filter(Player.id == player1_id).first()
    player2 = db.query(Player).filter(Player.id == player2_id).first()
    
    if not player1 or not player2:
        raise HTTPException(status_code=404, detail="Um ou ambos os jogadores não encontrados")
    
    # Ordenar os IDs para garantir consistência
    low_id = min(player1_id, player2_id)
    high_id = max(player1_id, player2_id)
    
    h2h = db.query(PlayerVsPlayer).filter(
        PlayerVsPlayer.player1_id == low_id,
        PlayerVsPlayer.player2_id == high_id
    ).first()
    
    if not h2h:
        # Se não encontrou registro, significa que nunca jogaram um contra o outro
        return {
            "player1": player1,
            "player2": player2,
            "matchup_description": f"{player1.name} vs {player2.name}",  # Added field
            "total_matches": 0,
            "player1_wins": 0,
            "player2_wins": 0,
            "hard_court": {"total": 0, "player1_wins": 0, "player2_wins": 0},
            "clay_court": {"total": 0, "player1_wins": 0, "player2_wins": 0},
            "grass_court": {"total": 0, "player1_wins": 0, "player2_wins": 0},
            "carpet_court": {"total": 0, "player1_wins": 0, "player2_wins": 0},
            "indoor": {"total": 0, "player1_wins": 0, "player2_wins": 0},
            "outdoor": {"total": 0, "player1_wins": 0, "player2_wins": 0},
            "tournaments": {}
        }
    
    # Ajustar os resultados com base na ordem dos jogadores
    if player1_id == h2h.player1_id:
        player1_wins = h2h.player1_wins
        player2_wins = h2h.player2_wins
        
        hard_court = {
            "total": h2h.hard_court_matches,
            "player1_wins": h2h.hard_court_player1_wins,
            "player2_wins": h2h.hard_court_player2_wins
        }
        clay_court = {
            "total": h2h.clay_court_matches,
            "player1_wins": h2h.clay_court_player1_wins,
            "player2_wins": h2h.clay_court_player2_wins
        }
        grass_court = {
            "total": h2h.grass_court_matches,
            "player1_wins": h2h.grass_court_player1_wins,
            "player2_wins": h2h.grass_court_player2_wins
        }
        carpet_court = {
            "total": h2h.carpet_court_matches,
            "player1_wins": h2h.carpet_court_player1_wins,
            "player2_wins": h2h.carpet_court_player2_wins
        }
        indoor = {
            "total": h2h.indoor_matches,
            "player1_wins": h2h.indoor_player1_wins,
            "player2_wins": h2h.indoor_player2_wins
        }
        outdoor = {
            "total": h2h.outdoor_matches,
            "player1_wins": h2h.outdoor_player1_wins,
            "player2_wins": h2h.outdoor_player2_wins
        }
    else:
        player1_wins = h2h.player2_wins
        player2_wins = h2h.player1_wins
        
        hard_court = {
            "total": h2h.hard_court_matches,
            "player1_wins": h2h.hard_court_player2_wins,
            "player2_wins": h2h.hard_court_player1_wins
        }
        clay_court = {
            "total": h2h.clay_court_matches,
            "player1_wins": h2h.clay_court_player2_wins,
            "player2_wins": h2h.clay_court_player1_wins
        }
        grass_court = {
            "total": h2h.grass_court_matches,
            "player1_wins": h2h.grass_court_player2_wins,
            "player2_wins": h2h.grass_court_player1_wins
        }
        carpet_court = {
            "total": h2h.carpet_court_matches,
            "player1_wins": h2h.carpet_court_player2_wins,
            "player2_wins": h2h.carpet_court_player1_wins
        }
        indoor = {
            "total": h2h.indoor_matches,
            "player1_wins": h2h.indoor_player2_wins,
            "player2_wins": h2h.indoor_player1_wins
        }
        outdoor = {
            "total": h2h.outdoor_matches,
            "player1_wins": h2h.outdoor_player2_wins,
            "player2_wins": h2h.outdoor_player1_wins
        }
    
    # Obter estatísticas por torneio
    query = db.query(
        Tournament.id,
        Tournament.name,
        func.count(TennisMatch.id).label("total"),
        func.sum(TennisMatch.winner_id == player1_id).label("player1_wins"),
        func.sum(TennisMatch.winner_id == player2_id).label("player2_wins")
    ).join(
        TennisMatch, Tournament.id == TennisMatch.tournament_id
    ).filter(
        or_(
            and_(TennisMatch.player1_id == player1_id, TennisMatch.player2_id == player2_id),
            and_(TennisMatch.player1_id == player2_id, TennisMatch.player2_id == player1_id)
        )
    ).group_by(
        Tournament.id, Tournament.name
    )
    
    tournaments_results = query.all()
    tournaments = {}
    for result in tournaments_results:
        tournaments[result.name] = {
            "id": result.id,
            "total": result.total,
            "player1_wins": result.player1_wins,
            "player2_wins": result.player2_wins
        }
    
    return {
        "player1": player1,
        "player2": player2,
        "matchup_description": f"{player1.name} vs {player2.name}",  # Populate new field
        "total_matches": h2h.total_matches,
        "player1_wins": player1_wins,
        "player2_wins": player2_wins,
        "hard_court": hard_court,
        "clay_court": clay_court,
        "grass_court": grass_court,
        "carpet_court": carpet_court,
        "indoor": indoor,
        "outdoor": outdoor,
        "tournaments": tournaments
    }

@router.get("/api/tennis/top-players", response_model=List[PlayerEloModel])
def get_top_players(surface: Optional[str] = None, limit: int = 20, db: Session = Depends(get_db)):
    """
    Obter os melhores jogadores classificados por ELO.
    Pode filtrar por tipo de superfície.
    """
    query = db.query(PlayerElo, Player.name).join(Player).order_by(PlayerElo.elo_rating.desc())
    
    if surface:
        surface = surface.lower()
        if "hard" in surface:
            query = query.order_by(PlayerElo.hard_court_elo.desc())
        elif "clay" in surface:
            query = query.order_by(PlayerElo.clay_court_elo.desc())
        elif "grass" in surface:
            query = query.order_by(PlayerElo.grass_court_elo.desc())
        elif "carpet" in surface:
            query = query.order_by(PlayerElo.carpet_court_elo.desc())
        elif "indoor" in surface:
            query = query.order_by(PlayerElo.indoor_elo.desc())
        elif "outdoor" in surface:
            query = query.order_by(PlayerElo.outdoor_elo.desc())
        else:
            query = query.order_by(PlayerElo.elo_rating.desc())
    else:
        query = query.order_by(PlayerElo.elo_rating.desc())
    
    results = query.limit(limit).all()
    
    return [
        {
            "player_id": elo.player_id,
            "player_name": name,
            "elo_rating": elo.elo_rating,
            "hard_court_elo": elo.hard_court_elo,
            "clay_court_elo": elo.clay_court_elo,
            "grass_court_elo": elo.grass_court_elo,
            "carpet_court_elo": elo.carpet_court_elo,
            "indoor_elo": elo.indoor_elo,
            "outdoor_elo": elo.outdoor_elo
        }
        for elo, name in results
    ]

@router.get("/api/tennis/player/{player_id}/tournament/{tournament_id}/stats")
def get_player_tournament_performance(player_id: int, tournament_id: int, db: Session = Depends(get_db)):
    """
    Obter desempenho detalhado de um jogador em um torneio específico,
    incluindo estatísticas gerais e confrontos
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneio não encontrado")
    
    # Obter estatísticas do jogador no torneio
    stats = player.get_tournament_stats(tournament_id, db)
    
    # Obter partidas do jogador neste torneio
    matches = player.get_matches_in_tournament(tournament_id, db)
    
    # Processar dados das partidas
    processed_matches = []
    for match in matches:
        opponent_id = match.player2_id if match.player1_id == player_id else match.player1_id
        opponent = db.query(Player).filter(Player.id == opponent_id).first()
        
        processed_matches.append({
            "match_id": match.id,
            "date": match.date.isoformat(),
            "round": match.round,
            "opponent_id": opponent_id,
            "opponent_name": opponent.name if opponent else "Desconhecido",
            "result": "Vitória" if match.winner_id == player_id else "Derrota",
            "score": match.score
        })
    
    # Retornar dados compilados
    return {
        "player": {
            "id": player.id,
            "name": player.name
        },
        "tournament": {
            "id": tournament.id,
            "name": tournament.name,
            "surface": tournament.surface,
            "court": tournament.court
        },
        "statistics": {
            "appearances": stats.appearances if stats else 0,
            "wins": stats.wins if stats else 0,
            "losses": stats.losses if stats else 0,
            "win_percentage": (stats.wins / stats.appearances * 100) if stats and stats.appearances > 0 else 0,
            "hard_court_wins": stats.hard_court_wins if stats else 0,
            "clay_court_wins": stats.clay_court_wins if stats else 0,
            "grass_court_wins": stats.grass_court_wins if stats else 0,
            "carpet_court_wins": stats.carpet_court_wins if stats else 0,
            "indoor_wins": stats.indoor_wins if stats else 0,
            "outdoor_wins": stats.outdoor_wins if stats else 0
        },
        "matches": processed_matches
    }

@router.get("/api/tennis/player/{player_id}/tournaments/matchups")
def get_player_tournament_matchups(player_id: int, db: Session = Depends(get_db)):
    """
    Obter todos os confrontos de um jogador agrupados por torneio,
    mostrando os oponentes em cada torneio
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    # Obter todos os torneios em que o jogador participou
    tournaments = player.tournaments
    
    result = []
    for tournament in tournaments:
        # Obter todas as partidas do jogador neste torneio
        matches = db.query(TennisMatch).filter(
            TennisMatch.tournament_id == tournament.id,
            or_(
                TennisMatch.player1_id == player_id,
                TennisMatch.player2_id == player_id
            )
        ).all()
        
        # Agrupar oponentes
        opponents = {}
        for match in matches:
            opponent_id = match.player2_id if match.player1_id == player_id else match.player1_id
            if opponent_id not in opponents:
                opponent = db.query(Player).filter(Player.id == opponent_id).first()
                opponents[opponent_id] = {
                    "id": opponent_id,
                    "name": opponent.name if opponent else "Desconhecido",
                    "matches": 0,
                    "wins": 0,
                    "losses": 0
                }
            
            opponents[opponent_id]["matches"] += 1
            if match.winner_id == player_id:
                opponents[opponent_id]["wins"] += 1
            else:
                opponents[opponent_id]["losses"] += 1
        
        result.append({
            "tournament_id": tournament.id,
            "tournament_name": tournament.name,
            "opponents": list(opponents.values())
        })
    
    return result

@router.get("/api/tennis/tournament/{tournament_id}/matchups")
def get_tournament_matchups(tournament_id: int, db: Session = Depends(get_db)):
    """
    Obter todos os confrontos diretos que ocorreram em um torneio específico
    """
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneio não encontrado")
    
    # Buscar todos os pares únicos de jogadores que se enfrentaram neste torneio
    matchups = db.query(
        func.least(TennisMatch.player1_id, TennisMatch.player2_id).label('p1_id'),
        func.greatest(TennisMatch.player1_id, TennisMatch.player2_id).label('p2_id'),
        func.count(TennisMatch.id).label('matches_count')
    ).filter(
        TennisMatch.tournament_id == tournament_id
    ).group_by(
        'p1_id', 'p2_id'
    ).all()
    
    result = []
    for matchup in matchups:
        player1 = db.query(Player).filter(Player.id == matchup.p1_id).first()
        player2 = db.query(Player).filter(Player.id == matchup.p2_id).first()
        
        if player1 and player2:
            # Contar vitórias de cada jogador
            player1_wins = db.query(func.count(TennisMatch.id)).filter(
                TennisMatch.tournament_id == tournament_id,
                or_(
                    and_(TennisMatch.player1_id == player1.id, TennisMatch.player2_id == player2.id),
                    and_(TennisMatch.player1_id == player2.id, TennisMatch.player2_id == player1.id)
                ),
                TennisMatch.winner_id == player1.id
            ).scalar()
            
            player2_wins = db.query(func.count(TennisMatch.id)).filter(
                TennisMatch.tournament_id == tournament_id,
                or_(
                    and_(TennisMatch.player1_id == player1.id, TennisMatch.player2_id == player2.id),
                    and_(TennisMatch.player1_id == player2.id, TennisMatch.player2_id == player1.id)
                ),
                TennisMatch.winner_id == player2.id
            ).scalar()
            
            result.append({
                "player1_id": player1.id,
                "player1_name": player1.name,
                "player2_id": player2.id,
                "player2_name": player2.name,
                "matches_count": matchup.matches_count,
                "player1_wins": player1_wins,
                "player2_wins": player2_wins,
                "tournament_id": tournament_id,
                "tournament_name": tournament.name
            })
    
    return result

@router.get("/api/tennis/integrated-data")
def get_integrated_tennis_data(
    player_id: Optional[int] = None,
    tournament_id: Optional[int] = None,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Endpoint integrado que retorna dados relacionados de jogadores, 
    torneios e confrontos diretos
    """
    result = {
        "top_players": [],
        "top_tournaments": [],
        "notable_matchups": []
    }
    
    # Se um jogador específico foi solicitado
    if player_id:
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")
        
        # Obter torneios do jogador, ordenados por número de vitórias
        tournaments_query = select([
            Tournament.id,
            Tournament.name,
            player_tournament.c.wins,
            player_tournament.c.appearances
        ]).select_from(
            player_tournament.join(Tournament, Tournament.id == player_tournament.c.tournament_id)
        ).where(
            player_tournament.c.player_id == player_id
        ).order_by(
            player_tournament.c.wins.desc()
        ).limit(limit)
        
        top_tournaments = db.execute(tournaments_query).all()
        
        # Obter confrontos mais frequentes do jogador
        h2h_query = db.query(
            PlayerVsPlayer,
            func.greatest(PlayerVsPlayer.player1_wins, PlayerVsPlayer.player2_wins).label('max_wins')
        ).filter(
            or_(
                PlayerVsPlayer.player1_id == player_id,
                PlayerVsPlayer.player2_id == player_id
            )
        ).order_by(
            PlayerVsPlayer.total_matches.desc()
        ).limit(limit)
        
        top_matchups = h2h_query.all()
        
        result["player"] = {
            "id": player.id,
            "name": player.name,
            "tournaments": [
                {
                    "tournament_id": t.id,
                    "tournament_name": t.name,
                    "wins": t.wins,
                    "appearances": t.appearances,
                    "win_rate": (t.wins / t.appearances * 100) if t.appearances > 0 else 0
                } 
                for t in top_tournaments
            ],
            "rivals": [
                {
                    "h2h_id": h2h[0].id,
                    "opponent_id": h2h[0].player2_id if h2h[0].player1_id == player_id else h2h[0].player1_id,
                    "opponent_name": h2h[0].player2_name if h2h[0].player1_id == player_id else h2h[0].player1_name,
                    "total_matches": h2h[0].total_matches,
                    "player_wins": h2h[0].player1_wins if h2h[0].player1_id == player_id else h2h[0].player2_wins,
                    "opponent_wins": h2h[0].player2_wins if h2h[0].player1_id == player_id else h2h[0].player1_wins,
                    "rivalry_summary": h2h[0].rivalry_summary
                }
                for h2h in top_matchups
            ]
        }
    
    # Se um torneio específico foi solicitado
    if tournament_id:
        tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
        if not tournament:
            raise HTTPException(status_code=404, detail="Torneio não encontrado")
        
        # Obter jogadores mais bem-sucedidos neste torneio
        top_players_query = select([
            Player.id,
            Player.name,
            player_tournament.c.wins,
            player_tournament.c.appearances
        ]).select_from(
            player_tournament.join(Player, Player.id == player_tournament.c.player_id)
        ).where(
            player_tournament.c.tournament_id == tournament_id,
            player_tournament.c.appearances > 0
        ).order_by(
            (player_tournament.c.wins / player_tournament.c.appearances).desc(),
            player_tournament.c.wins.desc()
        ).limit(limit)
        
        top_players = db.execute(top_players_query).all()
        
        # Obter confrontos mais memoráveis neste torneio
        memorable_matches_query = db.query(TennisMatch).filter(
            TennisMatch.tournament_id == tournament_id
        ).order_by(
            TennisMatch.date.desc()
        ).limit(limit)
        
        memorable_matches = memorable_matches_query.all()
        
        result["tournament"] = {
            "id": tournament.id,
            "name": tournament.name,
            "surface": tournament.surface,
            "court": tournament.court,
            "top_players": [
                {
                    "player_id": p.id,
                    "player_name": p.name,
                    "wins": p.wins,
                    "appearances": p.appearances,
                    "win_rate": (p.wins / p.appearances * 100) if p.appearances > 0 else 0
                }
                for p in top_players
            ],
            "memorable_matches": [
                {
                    "match_id": m.id,
                    "date": m.date.isoformat(),
                    "round": m.round,
                    "player1_id": m.player1_id,
                    "player1_name": m.player1.name,
                    "player2_id": m.player2_id,
                    "player2_name": m.player2.name,
                    "winner_id": m.winner_id,
                    "winner_name": m.winner.name,
                    "score": m.score
                }
                for m in memorable_matches
            ]
        }
    
    # Se nenhum jogador ou torneio específico foi solicitado, retornar dados gerais
    if not player_id and not tournament_id:
        # Top jogadores por ELO
        top_players_query = db.query(PlayerElo, Player.name).join(
            Player
        ).order_by(
            PlayerElo.elo_rating.desc()
        ).limit(limit)
        
        result["top_players"] = [
            {
                "player_id": p[0].player_id,
                "player_name": p[1],
                "elo_rating": p[0].elo_rating
            }
            for p in top_players_query.all()
        ]
        
        # Torneios com mais partidas
        top_tournaments_query = db.query(
            Tournament.id,
            Tournament.name,
            func.count(TennisMatch.id).label('matches_count')
        ).join(
            TennisMatch
        ).group_by(
            Tournament.id,
            Tournament.name
        ).order_by(
            func.count(TennisMatch.id).desc()
        ).limit(limit)
        
        result["top_tournaments"] = [
            {
                "tournament_id": t.id,
                "tournament_name": t.name,
                "matches_count": t.matches_count
            }
            for t in top_tournaments_query.all()
        ]
        
        # Confrontos mais frequentes
        top_matchups_query = db.query(
            PlayerVsPlayer
        ).order_by(
            PlayerVsPlayer.total_matches.desc()
        ).limit(limit)
        
        result["notable_matchups"] = [
            {
                "player1_id": h2h.player1_id,
                "player1_name": h2h.player1_name,
                "player2_id": h2h.player2_id,
                "player2_name": h2h.player2_name,
                "total_matches": h2h.total_matches,
                "player1_wins": h2h.player1_wins,
                "player2_wins": h2h.player2_wins,
                "rivalry_summary": h2h.rivalry_summary
            }
            for h2h in top_matchups_query.all()
        ]
    
    return result
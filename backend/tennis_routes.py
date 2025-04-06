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
        orm_mode = True

class TournamentModel(BaseModel):
    id: int
    name: str
    series: Optional[str]
    court: Optional[str]
    surface: Optional[str]
    
    class Config:
        orm_mode = True

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
        orm_mode = True

class PlayerTournamentStats(BaseModel):
    player_id: int
    player_name: str
    tournament_id: int
    tournament_name: str
    appearances: int
    wins: int
    best_round: Optional[str]
    
    class Config:
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

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
            "player_name": result.player_name,
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
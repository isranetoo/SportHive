from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)

class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)

# Tabela de associação entre jogadores e torneios expandida
player_tournament = Table(
    "player_tournament",
    Base.metadata,
    Column("player_id", Integer, ForeignKey("players.id"), primary_key=True),
    Column("tournament_id", Integer, ForeignKey("tournaments.id"), primary_key=True),
    Column("appearances", Integer, default=0),  # Número de aparições no torneio
    Column("wins", Integer, default=0),  # Número de vitórias no torneio
    Column("losses", Integer, default=0),  # Número de derrotas no torneio
    Column("best_round", String, nullable=True),  # Melhor fase alcançada
    Column("hard_court_wins", Integer, default=0),  # Vitórias em quadra dura
    Column("clay_court_wins", Integer, default=0),  # Vitórias em saibro
    Column("grass_court_wins", Integer, default=0),  # Vitórias em grama
    Column("carpet_court_wins", Integer, default=0),  # Vitórias em carpet
    Column("indoor_wins", Integer, default=0),  # Vitórias indoor
    Column("outdoor_wins", Integer, default=0),  # Vitórias outdoor
    Column("elo_rating", Float, default=1500.0),  # Rating ELO no torneio
)

# Nova tabela para histórico de confrontos diretos
class PlayerVsPlayer(Base):
    __tablename__ = "player_vs_player"
    
    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    total_matches = Column(Integer, default=0)
    player1_wins = Column(Integer, default=0)
    player2_wins = Column(Integer, default=0)
    
    # Estatísticas por superfície (garantindo que todos tenham valor padrão 0)
    hard_court_matches = Column(Integer, default=0)
    hard_court_player1_wins = Column(Integer, default=0)
    hard_court_player2_wins = Column(Integer, default=0)
    
    clay_court_matches = Column(Integer, default=0)
    clay_court_player1_wins = Column(Integer, default=0)
    clay_court_player2_wins = Column(Integer, default=0)
    
    grass_court_matches = Column(Integer, default=0)
    grass_court_player1_wins = Column(Integer, default=0)
    grass_court_player2_wins = Column(Integer, default=0)
    
    carpet_court_matches = Column(Integer, default=0)
    carpet_court_player1_wins = Column(Integer, default=0)
    carpet_court_player2_wins = Column(Integer, default=0)
    
    # Estatísticas indoor/outdoor
    indoor_matches = Column(Integer, default=0)
    indoor_player1_wins = Column(Integer, default=0)
    indoor_player2_wins = Column(Integer, default=0)
    
    outdoor_matches = Column(Integer, default=0)
    outdoor_player1_wins = Column(Integer, default=0)
    outdoor_player2_wins = Column(Integer, default=0)
    
    # Relacionamentos
    player1 = relationship("Player", foreign_keys=[player1_id], backref="head_to_head_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], backref="head_to_head_as_player2")

class PlayerElo(Base):
    __tablename__ = "player_elo"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    elo_rating = Column(Float, default=1500.0)  # Rating ELO geral
    hard_court_elo = Column(Float, default=1500.0)  # ELO em quadra dura
    clay_court_elo = Column(Float, default=1500.0)  # ELO em saibro
    grass_court_elo = Column(Float, default=1500.0)  # ELO em grama
    carpet_court_elo = Column(Float, default=1500.0)  # ELO em carpet
    indoor_elo = Column(Float, default=1500.0)  # ELO indoor
    outdoor_elo = Column(Float, default=1500.0)  # ELO outdoor
    active = Column(Boolean, default=True)  # Se o jogador está ativo
    last_updated = Column(Date, nullable=True)  # Data da última atualização
    
    # Relacionamento
    player = relationship("Player", backref="elo_rating_record")

# Modelos para os dados de tênis ATP
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    # Relationships
    matches_as_player1 = relationship("TennisMatch", foreign_keys="TennisMatch.player1_id", back_populates="player1")
    matches_as_player2 = relationship("TennisMatch", foreign_keys="TennisMatch.player2_id", back_populates="player2")
    matches_as_winner = relationship("TennisMatch", foreign_keys="TennisMatch.winner_id", back_populates="winner")
    
    # Relação muitos-para-muitos com torneios
    tournaments = relationship("Tournament", secondary=player_tournament, back_populates="players")
    
    # Método para obter confrontos contra um jogador específico
    def get_head_to_head(self, opponent_id, db):
        """Retorna o histórico de confrontos contra um oponente específico"""
        # Procura primeiro com player1 = self
        h2h = db.query(PlayerVsPlayer).filter(
            PlayerVsPlayer.player1_id == self.id,
            PlayerVsPlayer.player2_id == opponent_id
        ).first()
        
        if h2h:
            return {
                'total_matches': h2h.total_matches,
                'wins': h2h.player1_wins,
                'losses': h2h.player2_wins
            }
        
        # Se não encontrou, procura com player2 = self
        h2h = db.query(PlayerVsPlayer).filter(
            PlayerVsPlayer.player1_id == opponent_id,
            PlayerVsPlayer.player2_id == self.id
        ).first()
        
        if h2h:
            return {
                'total_matches': h2h.total_matches,
                'wins': h2h.player2_wins,
                'losses': h2h.player1_wins
            }
            
        # Se não encontrou nenhum
        return {
            'total_matches': 0,
            'wins': 0,
            'losses': 0
        }

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    series = Column(String, nullable=True)
    court = Column(String, nullable=True)
    surface = Column(String, nullable=True)
    
    # Relationships
    matches = relationship("TennisMatch", back_populates="tournament")
    
    # Nova relação muitos-para-muitos com jogadores
    players = relationship("Player", secondary=player_tournament, back_populates="tournaments")

class TennisMatch(Base):
    __tablename__ = "tennis_matches"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    date = Column(Date, nullable=False)
    round = Column(String, nullable=False)
    best_of = Column(Integer, nullable=False)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    rank1 = Column(Integer, nullable=True)
    rank2 = Column(Integer, nullable=True)
    pts1 = Column(Integer, nullable=True)
    pts2 = Column(Integer, nullable=True)
    odd1 = Column(Float, nullable=True)
    odd2 = Column(Float, nullable=True)
    score = Column(String, nullable=True)
    
    # Relationships
    tournament = relationship("Tournament", back_populates="matches")
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="matches_as_player2")
    winner = relationship("Player", foreign_keys=[winner_id], back_populates="matches_as_winner")

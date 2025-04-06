from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table, Boolean, select, or_
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
    
    matchup_description = Column(String, nullable=True)  # New field
    
    # Relacionamentos
    player1 = relationship("Player", foreign_keys=[player1_id], backref="head_to_head_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], backref="head_to_head_as_player2")

    @property
    def player1_name(self):
        """Retorna o nome do jogador 1"""
        return self.player1.name if self.player1 else None

    @property
    def player2_name(self):
        """Retorna o nome do jogador 2"""
        return self.player2.name if self.player2 else None
    
    # Novo método para obter partidas por torneio
    def get_matches_by_tournament(self, db):
        """Retorna as partidas entre os dois jogadores agrupadas por torneio"""
        from sqlalchemy import or_, and_, func
        
        matches_by_tournament = db.query(
            Tournament.id,
            Tournament.name,
            func.count(TennisMatch.id).label('match_count')
        ).join(
            TennisMatch, 
            Tournament.id == TennisMatch.tournament_id
        ).filter(
            or_(
                and_(
                    TennisMatch.player1_id == self.player1_id,
                    TennisMatch.player2_id == self.player2_id
                ),
                and_(
                    TennisMatch.player1_id == self.player2_id,
                    TennisMatch.player2_id == self.player1_id
                )
            )
        ).group_by(
            Tournament.id,
            Tournament.name
        ).all()
        
        return matches_by_tournament
    
    # Propriedades para facilitar o acesso às percentagens de vitória
    @property
    def player1_win_percentage(self):
        """Percentagem de vitórias do jogador 1"""
        if self.total_matches == 0:
            return 0
        return (self.player1_wins / self.total_matches) * 100
    
    @property
    def player2_win_percentage(self):
        """Percentagem de vitórias do jogador 2"""
        if self.total_matches == 0:
            return 0
        return (self.player2_wins / self.total_matches) * 100
    
    @property
    def rivalry_summary(self):
        """Resumo da rivalidade entre os jogadores"""
        if self.total_matches == 0:
            return f"Sem confrontos entre {self.player1_name} e {self.player2_name}"
            
        diff = abs(self.player1_wins - self.player2_wins)
        
        if diff == 0:
            return f"Rivalidade equilibrada: {self.player1_wins}-{self.player2_wins}"
        
        leading_player = self.player1_name if self.player1_wins > self.player2_wins else self.player2_name
        leading_wins = max(self.player1_wins, self.player2_wins)
        trailing_wins = min(self.player1_wins, self.player2_wins)
        
        return f"{leading_player} lidera {leading_wins}-{trailing_wins}"

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
    ranking = Column(Integer, nullable=True)  # Ranking do jogador
    country = Column(String, nullable=True)  # País do jogador
    titles = Column(Integer, default=0)  # Número de títulos
    grand_slams = Column(Integer, default=0)  # Número de Grand Slams
    hand = Column(String, nullable=True)  # Mão dominante (esquerda/direita)
    img_url = Column(String, nullable=True)  # URL da imagem do jogador
    
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
    
    # Novos métodos para relacionar jogadores, torneios e confrontos
    def get_tournament_stats(self, tournament_id, db):
        """Retorna estatísticas do jogador em um torneio específico"""
        from sqlalchemy import and_
        stats = db.execute(
            select([player_tournament]).where(
                and_(
                    player_tournament.c.player_id == self.id,
                    player_tournament.c.tournament_id == tournament_id
                )
            )
        ).first()
        return stats

    def get_all_opponents(self, db):
        """Retorna todos os oponentes que já enfrentou com estatísticas"""
        # Busca todos os jogadores enfrentados como player1
        h2h_as_player1 = db.query(PlayerVsPlayer).filter(
            PlayerVsPlayer.player1_id == self.id
        ).all()
        
        # Busca todos os jogadores enfrentados como player2
        h2h_as_player2 = db.query(PlayerVsPlayer).filter(
            PlayerVsPlayer.player2_id == self.id
        ).all()
        
        opponents = []
        
        # Processa os dados onde é o player1
        for h2h in h2h_as_player1:
            opponents.append({
                'opponent_id': h2h.player2_id,
                'opponent_name': h2h.player2_name,
                'matches': h2h.total_matches,
                'wins': h2h.player1_wins,
                'losses': h2h.player2_wins
            })
        
        # Processa os dados onde é o player2
        for h2h in h2h_as_player2:
            opponents.append({
                'opponent_id': h2h.player1_id,
                'opponent_name': h2h.player1_name,
                'matches': h2h.total_matches,
                'wins': h2h.player2_wins,
                'losses': h2h.player1_wins
            })
        
        return opponents
    
    def get_matches_in_tournament(self, tournament_id, db):
        """Retorna todas as partidas do jogador em um torneio específico"""
        matches = db.query(TennisMatch).filter(
            TennisMatch.tournament_id == tournament_id,
            or_(
                TennisMatch.player1_id == self.id,
                TennisMatch.player2_id == self.id
            )
        ).all()
        return matches

    def get_most_common_opponents(self, limit=5, db=None):
        """Retorna os oponentes mais frequentes"""
        from sqlalchemy import func, or_, and_
        
        if db is None:
            return []
            
        # Conta o número de partidas contra cada oponente
        opponent_counts = db.query(
            Player.id.label('opponent_id'),
            Player.name.label('opponent_name'),
            func.count(TennisMatch.id).label('match_count')
        ).join(
            TennisMatch,
            or_(
                and_(TennisMatch.player1_id == Player.id, TennisMatch.player2_id == self.id),
                and_(TennisMatch.player2_id == Player.id, TennisMatch.player1_id == self.id)
            )
        ).filter(
            Player.id != self.id
        ).group_by(
            Player.id, 
            Player.name
        ).order_by(
            func.count(TennisMatch.id).desc()
        ).limit(limit).all()
        
        return opponent_counts

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    series = Column(String, nullable=True)
    court = Column(String, nullable=True)
    surface = Column(String, nullable=True)
    location = Column(String, nullable=True)  # Localização do torneio
    date = Column(String, nullable=True)  # Data do torneio
    prize = Column(String, nullable=True)  # Prêmio do torneio
    img_url = Column(String, nullable=True)  # URL da imagem do torneio
    
    # Relationships
    matches = relationship("TennisMatch", back_populates="tournament")
    
    # Nova relação muitos-para-muitos com jogadores
    players = relationship("Player", secondary=player_tournament, back_populates="tournaments")
    
    # Novos métodos para relacionar torneios, jogadores e confrontos
    def get_all_matches(self, db):
        """Retorna todas as partidas do torneio"""
        return db.query(TennisMatch).filter(TennisMatch.tournament_id == self.id).all()
    
    def get_player_stats(self, player_id, db):
        """Retorna estatísticas de um jogador específico neste torneio"""
        from sqlalchemy import and_
        stats = db.execute(
            select([player_tournament]).where(
                and_(
                    player_tournament.c.tournament_id == self.id,
                    player_tournament.c.player_id == player_id
                )
            )
        ).first()
        return stats
    
    def get_top_performers(self, limit=5, db=None):
        """Retorna os jogadores com melhor desempenho neste torneio"""
        if db is None:
            return []
            
        from sqlalchemy import desc
        
        query = select([
            player_tournament.c.player_id,
            Player.name,
            player_tournament.c.wins,
            player_tournament.c.appearances,
            (player_tournament.c.wins * 100 / player_tournament.c.appearances).label('win_percentage')
        ]).select_from(
            player_tournament.join(
                Player, 
                player_tournament.c.player_id == Player.id
            )
        ).where(
            player_tournament.c.tournament_id == self.id,
            player_tournament.c.appearances > 0
        ).order_by(
            desc('win_percentage'), 
            desc(player_tournament.c.wins)
        ).limit(limit)
        
        return db.execute(query).all()
    
    def get_matchups(self, db):
        """Retorna os confrontos diretos que aconteceram neste torneio"""
        from sqlalchemy import func, and_, or_
        
        # Busca pares de jogadores que se enfrentaram neste torneio
        matchups = db.query(
            func.least(TennisMatch.player1_id, TennisMatch.player2_id).label('player1_id'),
            func.greatest(TennisMatch.player1_id, TennisMatch.player2_id).label('player2_id'),
            func.count(TennisMatch.id).label('matches_count')
        ).filter(
            TennisMatch.tournament_id == self.id
        ).group_by(
            'player1_id', 
            'player2_id'
        ).all()
        
        return matchups

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
    score = Column(String, nullable=True)
    rank1 = Column(Integer, nullable=True)
    rank2 = Column(Integer, nullable=True)
    pts1 = Column(Integer, nullable=True)
    pts2 = Column(Integer, nullable=True)
    odd1 = Column(Float, nullable=True)
    odd2 = Column(Float, nullable=True)
    
    # Relationships
    tournament = relationship("Tournament", back_populates="matches")
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="matches_as_player2")
    winner = relationship("Player", foreign_keys=[winner_id], back_populates="matches_as_winner")

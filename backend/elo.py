"""
Funções para calcular o rating ELO dos jogadores de tênis
"""

def calculate_expected_outcome(player_rating, opponent_rating):
    """
    Calcula o resultado esperado para o jogador baseado na diferença de ELO.
    Retorna um valor entre 0 e 1, representando a probabilidade de vitória.
    """
    return 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))

def update_elo(player_rating, opponent_rating, result, k_factor=32):
    """
    Atualiza o rating ELO do jogador com base no resultado da partida.
    
    Args:
        player_rating: Rating ELO atual do jogador
        opponent_rating: Rating ELO do oponente
        result: Resultado da partida (1 para vitória, 0 para derrota, 0.5 para empate)
        k_factor: Fator K, que determina o impacto máximo de uma partida (padrão: 32)
        
    Returns:
        Novo rating ELO do jogador
    """
    expected = calculate_expected_outcome(player_rating, opponent_rating)
    new_rating = player_rating + k_factor * (result - expected)
    return new_rating

def adjust_k_factor(player_rating, matches_played):
    """
    Ajusta o fator K com base no rating do jogador e no número de partidas jogadas.
    Jogadores com mais partidas ou ratings mais altos têm um fator K menor.
    
    Args:
        player_rating: Rating ELO atual do jogador
        matches_played: Número de partidas que o jogador já disputou
        
    Returns:
        Fator K ajustado
    """
    if matches_played < 30:
        # Jogadores novos têm oscilações maiores
        return 40
    elif player_rating < 2100:
        # Jogadores intermediários
        return 32
    elif player_rating < 2400:
        # Jogadores avançados
        return 24
    else:
        # Jogadores de elite
        return 16

def calculate_tournament_performance_rating(matches, player_id):
    """
    Calcula a classificação de desempenho do jogador em um torneio específico
    com base em sua performance contra os oponentes.
    
    Args:
        matches: Lista de partidas (cada uma com os jogadores e o vencedor)
        player_id: ID do jogador para o qual calcular o rating
        
    Returns:
        Rating de desempenho no torneio
    """
    if not matches:
        return 1500  # Rating padrão
    
    total_opponent_rating = 0
    matches_count = 0
    wins = 0
    
    for match in matches:
        if match.player1_id == player_id:
            opponent_id = match.player2_id
            if match.winner_id == player_id:
                wins += 1
        elif match.player2_id == player_id:
            opponent_id = match.player1_id
            if match.winner_id == player_id:
                wins += 1
        else:
            continue  # O jogador não participou dessa partida
        
        # Aqui você precisaria obter o rating do oponente do banco de dados
        # Simplificando para fins de demonstração
        opponent_rating = 1500  # Valor padrão
        
        total_opponent_rating += opponent_rating
        matches_count += 1
    
    if matches_count == 0:
        return 1500
    
    # Calcular o rating médio dos oponentes
    avg_opponent_rating = total_opponent_rating / matches_count
    
    # Calcular o rating de desempenho
    # Se o jogador venceu todas as partidas, seu rating deve ser maior que a média
    # Se perdeu todas, deve ser menor
    win_percentage = wins / matches_count
    performance_rating = avg_opponent_rating + 400 * (2 * win_percentage - 1)
    
    return performance_rating

def calculate_surface_adjustment(player_id, surface, db):
    """
    Calcula um ajuste de rating baseado no desempenho do jogador em uma superfície específica.
    
    Args:
        player_id: ID do jogador
        surface: Tipo de superfície (hard, clay, grass, carpet)
        db: Sessão do banco de dados
        
    Returns:
        Ajuste de rating para a superfície
    """
    # Aqui você implementaria a lógica para buscar estatísticas do jogador na superfície
    # e calcular um ajuste de rating
    
    # Implementação simplificada para demonstração
    return 0  # Sem ajuste

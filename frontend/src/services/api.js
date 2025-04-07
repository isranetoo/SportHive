import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/dataset";

// Configure axios with base URL
const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/tennis" // Ajuste para corresponder ao backend
});

// Add an interceptor for development to return mock data
api.interceptors.response.use(
    response => response,
    error => {
        // If we're in development and the API call fails, return mock data
        if (process.env.NODE_ENV === 'development' && error.response?.status === 404) {
            console.warn('Using mock data for development');
            
            // Check the URL to determine what mock data to return
            const url = error.config.url;
            
            if (url.includes('/tennis/players')) {
                return Promise.resolve({ 
                    data: Array(20).fill().map((_, i) => ({
                        id: i + 1,
                        name: `Player ${i + 1}`,
                        country: ['Spain', 'USA', 'Switzerland', 'Serbia', 'UK'][i % 5],
                        ranking: i + 1,
                        age: 20 + (i % 15),
                        titles: i * 2,
                        grandSlams: Math.floor(i / 5),
                        hand: i % 2 === 0 ? 'Right' : 'Left'
                    }))
                });
            }
            
            if (url.includes('/tennis/tournaments')) {
                return Promise.resolve({ 
                    data: Array(10).fill().map((_, i) => ({
                        id: i + 1,
                        name: ['Australian Open', 'Roland Garros', 'Wimbledon', 'US Open', 'Miami Open'][i % 5],
                        surface: ['Hard', 'Clay', 'Grass', 'Hard', 'Hard'][i % 5],
                        location: ['Melbourne', 'Paris', 'London', 'New York', 'Miami'][i % 5],
                        date: `2023-${(i % 12) + 1}-15`,
                        prize: `$${2 + i}M`,
                        series: i < 4 ? 'Grand Slam' : 'Masters 1000'
                    }))
                });
            }
            
            if (url.includes('/tennis/matches')) {
                return Promise.resolve({ 
                    data: Array(15).fill().map((_, i) => ({
                        id: i + 1,
                        player1: { id: i + 1, name: `Player ${i + 1}` },
                        player2: { id: i + 2, name: `Player ${i + 2}` },
                        winner: { id: i % 2 === 0 ? i + 1 : i + 2, name: i % 2 === 0 ? `Player ${i + 1}` : `Player ${i + 2}` },
                        tournament: { name: ['Australian Open', 'Roland Garros', 'Wimbledon', 'US Open', 'Miami Open'][i % 5] },
                        date: new Date().toISOString(),
                        round: ['Final', 'Semi-Final', 'Quarter-Final', 'R16', 'R32'][i % 5],
                        score: i % 2 === 0 ? '6-4, 7-5' : '6-3, 6-4, 7-6'
                    }))
                });
            }
            
            if (url.includes('/tennis/top-players')) {
                return Promise.resolve({ 
                    data: Array(20).fill().map((_, i) => ({
                        player_id: i + 1,
                        player_name: `Player ${i + 1}`,
                        elo_rating: 1500 + (20 - i) * 50,
                        hard_court_elo: 1500 + (20 - i) * 45 + (i % 3 === 0 ? 100 : 0),
                        clay_court_elo: 1500 + (20 - i) * 48 + (i % 3 === 1 ? 120 : 0),
                        grass_court_elo: 1500 + (20 - i) * 47 + (i % 3 === 2 ? 110 : 0),
                        carpet_court_elo: 1500 + (20 - i) * 46
                    }))
                });
            }
            
            if (url.includes('/tennis/head-to-head')) {
                return Promise.resolve({ 
                    data: {
                        player1: { id: 1, name: 'Player 1' },
                        player2: { id: 2, name: 'Player 2' },
                        total_matches: 25,
                        player1_wins: 15,
                        player2_wins: 10,
                        hard_court: { total: 10, player1_wins: 6, player2_wins: 4 },
                        clay_court: { total: 8, player1_wins: 5, player2_wins: 3 },
                        grass_court: { total: 5, player1_wins: 3, player2_wins: 2 },
                        carpet_court: { total: 2, player1_wins: 1, player2_wins: 1 },
                        tournaments: {
                            'Australian Open': { total: 5, player1_wins: 3, player2_wins: 2 },
                            'Roland Garros': { total: 6, player1_wins: 4, player2_wins: 2 },
                            'Wimbledon': { total: 4, player1_wins: 2, player2_wins: 2 },
                            'US Open': { total: 5, player1_wins: 3, player2_wins: 2 },
                            'Miami Open': { total: 5, player1_wins: 3, player2_wins: 2 }
                        }
                    }
                });
            }
        }
        
        // If not in development or not a 404, continue with the error
        return Promise.reject(error);
    }
);

export const fetchData = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar dados:", error);
        return null;
    }
};

export default api;

import React, { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { Link } from 'react-router-dom'
import api from '../services/api'

const TennisHeadToHead = () => {
  const [selectedPlayer1, setSelectedPlayer1] = useState('');
  const [selectedPlayer2, setSelectedPlayer2] = useState('');
  const [showResults, setShowResults] = useState(false);
  const [players, setPlayers] = useState([]);
  const [h2hData, setH2hData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch players on component mount
  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await api.get('/api/tennis/players');
        setPlayers(response.data);
      } catch (err) {
        console.error('Error fetching players data:', err);
        setError('Failed to load players data. Please try again later.');
      }
    };

    fetchPlayers();
  }, []);

  const handleCompare = async () => {
    if (selectedPlayer1 && selectedPlayer2) {
      try {
        setLoading(true);
        setError(null);
        
        // Changed from axios.get to api.get
        const response = await api.get(`/api/tennis/head-to-head-detailed?player1_id=${selectedPlayer1}&player2_id=${selectedPlayer2}`);
        setH2hData(response.data);
        setShowResults(true);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching head-to-head data:', err);
        setError('Failed to load head-to-head data. Please try again later.');
        setLoading(false);
      }
    }
  };

  // Function to format last five matches
  const formatLastFiveMatches = (h2hData) => {
    if (!h2hData || !h2hData.tournaments) return [];
    
    // Create an array from all tournament matches
    let allMatches = [];
    
    Object.entries(h2hData.tournaments).forEach(([tournamentName, data]) => {
      // Create simulated matches based on tournament data
      for (let i = 0; i < data.total; i++) {
        const isPlayer1Win = i < data.player1_wins;
        allMatches.push({
          tournament: tournamentName,
          winner: isPlayer1Win ? "player1" : "player2",
          score: isPlayer1Win ? "6-4, 7-5" : "6-3, 6-4", // Example scores
          year: new Date().getFullYear() - Math.floor(Math.random() * 5)
        });
      }
    });
    
    // Sort by year (desc) and take last 5
    return allMatches
      .sort((a, b) => b.year - a.year)
      .slice(0, 5);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="bg-blue-700 text-white py-14 relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-3xl">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Head to Head</h1>
              <p className="text-xl text-blue-100 mb-6">
                Compare o histórico de confrontos diretos entre os melhores tenistas do mundo.
              </p>
              <Link to="/tennis" className="bg-white text-blue-700 hover:bg-blue-50 py-3 px-6 rounded-lg font-medium transition-colors inline-flex items-center">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                </svg>
                Voltar para Tênis
              </Link>
            </div>
          </div>
          <div className="absolute right-0 bottom-0 w-1/3 h-full opacity-10">
            <img 
              src="https://images.unsplash.com/photo-1577471488278-16eec37ffcc2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
              alt="Tennis players" 
              className="w-full h-full object-cover object-center"
            />
          </div>
        </section>

        {/* Comparison Form */}
        <section className="py-12">
          <div className="container mx-auto px-4">
            <div className="bg-white rounded-xl shadow-md p-6 mb-10">
              <h2 className="text-2xl font-bold text-blue-900 mb-6">Selecione dois jogadores para comparar</h2>
              
              <div className="flex flex-col md:flex-row gap-6 mb-8">
                <div className="flex-1">
                  <label className="block text-gray-700 text-sm font-medium mb-2">Jogador 1</label>
                  <select 
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    value={selectedPlayer1}
                    onChange={(e) => setSelectedPlayer1(e.target.value)}
                  >
                    <option value="">Selecione um jogador</option>
                    {players.map((player) => (
                      <option key={player.id} value={player.id}>{player.name}</option>
                    ))}
                  </select>
                </div>
                
                <div className="flex items-center justify-center">
                  <span className="text-gray-500 text-2xl font-bold">VS</span>
                </div>
                
                <div className="flex-1">
                  <label className="block text-gray-700 text-sm font-medium mb-2">Jogador 2</label>
                  <select 
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    value={selectedPlayer2}
                    onChange={(e) => setSelectedPlayer2(e.target.value)}
                  >
                    <option value="">Selecione um jogador</option>
                    {players.map((player) => (
                      <option key={player.id} value={player.id}>{player.name}</option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div className="flex justify-center">
                <button 
                  onClick={handleCompare}
                  disabled={!selectedPlayer1 || !selectedPlayer2 || loading}
                  className={`py-3 px-8 rounded-lg font-medium flex items-center ${
                    (!selectedPlayer1 || !selectedPlayer2 || loading) 
                      ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {loading && (
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  )}
                  Comparar
                </button>
              </div>
              
              {error && (
                <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-lg text-center">
                  {error}
                </div>
              )}
            </div>
            
            {showResults && h2hData && (
              <div className="bg-white rounded-xl shadow-md overflow-hidden">
                <div className="p-6 bg-blue-50 border-b border-blue-100">
                  <h2 className="text-2xl font-bold text-blue-900">
                    {h2hData.player1.name} vs {h2hData.player2.name}
                  </h2>
                  <p className="text-blue-700">Histórico de confrontos diretos</p>
                </div>
                
                <div className="p-6">
                  <div className="flex flex-col md:flex-row mb-8">
                    <div className="flex-1 text-center p-4">
                      <div className="text-lg font-medium text-blue-800 mb-1">{h2hData.player1.name}</div>
                      <div className="text-5xl font-bold text-blue-600 mb-2">{h2hData.player1_wins}</div>
                      <div className="text-gray-500">Vitórias</div>
                    </div>
                    
                    <div className="flex-1 text-center p-4 border-t md:border-t-0 md:border-l md:border-r border-gray-200">
                      <div className="text-3xl font-bold text-gray-800 mb-2">{h2hData.total_matches}</div>
                      <div className="text-gray-500">Total de partidas</div>
                    </div>
                    
                    <div className="flex-1 text-center p-4">
                      <div className="text-lg font-medium text-red-800 mb-1">{h2hData.player2.name}</div>
                      <div className="text-5xl font-bold text-red-600 mb-2">{h2hData.player2_wins}</div>
                      <div className="text-gray-500">Vitórias</div>
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-6 mb-8">
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">Distribuição por superfície</h3>
                    
                    <div className="space-y-4">
                      {h2hData.hard_court.total > 0 && (
                        <div>
                          <div className="flex justify-between mb-1">
                            <span className="font-medium text-gray-700">Quadra dura</span>
                            <span className="text-gray-600">
                              <span className="text-blue-600">{h2hData.player1.name}: {h2hData.hard_court.player1_wins}</span>
                              {" - "}
                              <span className="text-red-600">{h2hData.player2.name}: {h2hData.hard_court.player2_wins}</span>
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div 
                              className="bg-blue-600 h-2.5 rounded-full" 
                              style={{ width: `${(h2hData.hard_court.player1_wins / h2hData.hard_court.total) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      )}
                      
                      {h2hData.clay_court.total > 0 && (
                        <div>
                          <div className="flex justify-between mb-1">
                            <span className="font-medium text-gray-700">Saibro</span>
                            <span className="text-gray-600">{h2hData.clay_court.player1_wins}-{h2hData.clay_court.player2_wins}</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div 
                              className="bg-blue-600 h-2.5 rounded-full" 
                              style={{ width: `${(h2hData.clay_court.player1_wins / h2hData.clay_court.total) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      )}
                      
                      {h2hData.grass_court.total > 0 && (
                        <div>
                          <div className="flex justify-between mb-1">
                            <span className="font-medium text-gray-700">Grama</span>
                            <span className="text-gray-600">{h2hData.grass_court.player1_wins}-{h2hData.grass_court.player2_wins}</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div 
                              className="bg-blue-600 h-2.5 rounded-full" 
                              style={{ width: `${(h2hData.grass_court.player1_wins / h2hData.grass_court.total) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      )}
                      
                      {h2hData.carpet_court.total > 0 && (
                        <div>
                          <div className="flex justify-between mb-1">
                            <span className="font-medium text-gray-700">Carpet</span>
                            <span className="text-gray-600">{h2hData.carpet_court.player1_wins}-{h2hData.carpet_court.player2_wins}</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div 
                              className="bg-blue-600 h-2.5 rounded-full" 
                              style={{ width: `${(h2hData.carpet_court.player1_wins / h2hData.carpet_court.total) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  {h2hData.total_matches > 0 && (
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">Últimas partidas</h3>
                      
                      <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                          <thead className="bg-gray-50">
                            <tr>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Torneio</th>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vencedor</th>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Placar</th>
                            </tr>
                          </thead>
                          <tbody className="bg-white divide-y divide-gray-200">
                            {Object.entries(h2hData.tournaments).slice(0, 5).map(([tournament, data], index) => (
                              <tr key={index} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{tournament}</td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                    data.player1_wins > data.player2_wins ? "bg-blue-100 text-blue-800" : "bg-red-100 text-red-800"
                                  }`}>
                                    {data.player1_wins > data.player2_wins ? h2hData.player1.name : h2hData.player2.name}
                                  </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{data.player1_wins}-{data.player2_wins}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}

export default TennisHeadToHead;

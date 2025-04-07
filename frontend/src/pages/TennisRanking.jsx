import React, { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { Link } from 'react-router-dom'
import api from '../services/api'

const TennisRanking = () => {
  const [rankingData, setRankingData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [surface, setSurface] = useState('');

  useEffect(() => {
    const fetchRanking = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/top-players${surface ? `?surface=${surface}` : ''}`); // Ajuste do endpoint
        
        // Make sure each player has all required fields with defaults if missing
        const processedData = response.data.map(player => ({
          ...player,
          player_name: player.player_name || "Desconhecido",
          elo_rating: player.elo_rating || 1500,
          hard_court_elo: player.hard_court_elo || 1500,
          clay_court_elo: player.clay_court_elo || 1500,
          grass_court_elo: player.grass_court_elo || 1500,
          carpet_court_elo: player.carpet_court_elo || 1500,
          indoor_elo: player.indoor_elo || 1500,
          outdoor_elo: player.outdoor_elo || 1500
        }));
        
        setRankingData(processedData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching ranking data:', err);
        setError('Failed to load ranking data. Please try again later.');
        setLoading(false);
      }
    };

    fetchRanking();
  }, [surface]);

  // Handle surface filter change
  const handleSurfaceChange = (newSurface) => {
    setSurface(newSurface);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="bg-blue-700 text-white py-14 relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-3xl">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Elo Ranking de Tênis</h1>
              <p className="text-xl text-blue-100 mb-6">
                Acompanhe a classificação dos melhores tenistas do mundo com base no sistema de pontuação Elo.
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
              src="https://images.unsplash.com/photo-1511886929837-354d827aae26?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
              alt="Tennis trophy" 
              className="w-full h-full object-cover object-center"
            />
          </div>
        </section>

        {/* Ranking Table Section */}
        <section className="py-12">
          <div className="container mx-auto px-4">
            {/* Surface Filter */}
            <div className="mb-6 flex flex-wrap gap-2 justify-center">
              <button 
                onClick={() => handleSurfaceChange('')}
                className={`py-2 px-4 rounded-lg ${!surface ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              >
                Geral
              </button>
              <button 
                onClick={() => handleSurfaceChange('hard')}
                className={`py-2 px-4 rounded-lg ${surface === 'hard' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              >
                Quadra Dura
              </button>
              <button 
                onClick={() => handleSurfaceChange('clay')}
                className={`py-2 px-4 rounded-lg ${surface === 'clay' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              >
                Saibro
              </button>
              <button 
                onClick={() => handleSurfaceChange('grass')}
                className={`py-2 px-4 rounded-lg ${surface === 'grass' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              >
                Grama
              </button>
              <button 
                onClick={() => handleSurfaceChange('indoor')}
                className={`py-2 px-4 rounded-lg ${surface === 'indoor' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              >
                Indoor
              </button>
            </div>

            {loading ? (
              <div className="flex justify-center items-center py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : error ? (
              <div className="text-center py-20">
                <div className="text-red-500 text-xl">{error}</div>
                <button 
                  onClick={() => window.location.reload()}
                  className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                  Tentar Novamente
                </button>
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-md overflow-hidden">
                <div className="p-6 bg-blue-50 border-b border-blue-100">
                  <h2 className="text-2xl font-bold text-blue-900">
                    Ranking ELO - {
                      !surface ? 'Geral' : 
                      surface === 'hard' ? 'Quadra Dura' :
                      surface === 'clay' ? 'Saibro' :
                      surface === 'grass' ? 'Grama' :
                      surface === 'indoor' ? 'Indoor' : 'Personalizado'
                    }
                  </h2>
                  <p className="text-blue-700">Os melhores jogadores classificados por pontuação ELO</p>
                </div>
                
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Posição
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Jogador
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Pontos ELO
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Hard
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Clay
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Grass
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {rankingData.map((player, index) => (
                        <tr key={player.player_id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{index + 1}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <Link to={`/tennis/players/${player.player_id}`} className="text-sm font-medium text-blue-600 hover:text-blue-800">
                              {player.player_name} {/* Changed from player_id to player_name */}
                            </Link>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-semibold text-gray-900">
                              {Math.round(player.elo_rating)}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">
                              {Math.round(player.hard_court_elo)}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">
                              {Math.round(player.clay_court_elo)}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">
                              {Math.round(player.grass_court_elo)}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
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

export default TennisRanking;

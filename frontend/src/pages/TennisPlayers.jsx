import React, { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { Link } from 'react-router-dom'
import api from '../services/api'

const TennisPlayers = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        setLoading(true);
        // Fixed API path from /tennis/players to /api/tennis/players
        const response = await api.get('/api/tennis/players');
        setPlayers(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching players data:', err);
        setError('Failed to load players data. Please try again later.');
        setLoading(false);
      }
    };

    fetchPlayers();
  }, []);

  // Filtragem de jogadores
  const filteredPlayers = players.filter(player => {
    const matchesSearch = player.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         (player.country && player.country.toLowerCase().includes(searchTerm.toLowerCase()));
    
    if (filter === 'all') return matchesSearch;
    // Note: These filters may need to be adjusted based on actual data properties
    if (filter === 'grandSlam') return matchesSearch && player.grand_slams > 0;
    if (filter === 'top5') return matchesSearch && player.ranking <= 5;
    
    return matchesSearch;
  });

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="bg-blue-700 text-white py-14 relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-3xl">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Jogadores de Tênis</h1>
              <p className="text-xl text-blue-100 mb-6">
                Conheça os melhores tenistas do circuito profissional, suas estatísticas e conquistas.
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
              src="https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
              alt="Tennis player" 
              className="w-full h-full object-cover object-center"
            />
          </div>
        </section>

        {/* Search and Filter Section */}
        <section className="py-8 bg-white shadow-md">
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
              <div className="w-full md:w-1/2">
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                  </div>
                  <input
                    type="text"
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Buscar por nome ou país..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
              
              <div className="w-full md:w-auto">
                <div className="flex flex-wrap justify-center gap-2">
                  <button 
                    onClick={() => setFilter('all')}
                    className={`py-2 px-4 rounded-lg font-medium ${
                      filter === 'all' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    Todos
                  </button>
                  <button 
                    onClick={() => setFilter('top5')}
                    className={`py-2 px-4 rounded-lg font-medium ${
                      filter === 'top5' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    Top 5
                  </button>
                  <button 
                    onClick={() => setFilter('grandSlam')}
                    className={`py-2 px-4 rounded-lg font-medium ${
                      filter === 'grandSlam' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    Campeões de Grand Slam
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Players Grid */}
        <section className="py-12">
          <div className="container mx-auto px-4">
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
              <>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                  {filteredPlayers.map((player) => (
                    <div key={player.id} className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow">
                      <div className="h-60 overflow-hidden bg-gray-200">
                        {/* Use a placeholder if no image URL is available */}
                        <img 
                          src={player.imgUrl || `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`} 
                          alt={player.name} 
                          className="w-full h-full object-cover object-center"
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
                          }}
                        />
                      </div>
                      <div className="p-6">
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <h3 className="text-xl font-semibold text-blue-900">{player.name}</h3>
                            <p className="text-gray-600">{player.country || "País não informado"}</p>
                          </div>
                          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                            {player.ranking || "?"}
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-3 mb-4">
                          <div className="bg-gray-50 rounded-lg p-3 text-center">
                            <div className="text-xs text-gray-500 uppercase">Jogador</div>
                            <div className="text-md font-bold text-blue-600">{player.name}</div>
                          </div>
                          
                          <div className="bg-gray-50 rounded-lg p-3 text-center">
                            <div className="text-2xl font-bold text-blue-600">{player.age || "?"}</div>
                            <div className="text-xs text-gray-500 uppercase">Idade</div>
                          </div>
                          
                          <div className="bg-gray-50 rounded-lg p-3 text-center">
                            <div className="text-2xl font-bold text-blue-600">{player.titles || "0"}</div>
                            <div className="text-xs text-gray-500 uppercase">Títulos</div>
                          </div>
                          
                          <div className="bg-gray-50 rounded-lg p-3 text-center">
                            <div className="text-2xl font-bold text-blue-600">{player.grandSlams || "0"}</div>
                            <div className="text-xs text-gray-500 uppercase">Grand Slams</div>
                          </div>
                          
                          <div className="bg-gray-50 rounded-lg p-3 text-center">
                            <div className="text-md font-bold text-blue-600">{player.hand || "N/A"}</div>
                            <div className="text-xs text-gray-500 uppercase">Mão</div>
                          </div>
                        </div>
                        
                        <Link to={`/tennis/players/${player.id}`} className="w-full block text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                          Ver Perfil
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
                
                {filteredPlayers.length === 0 && (
                  <div className="text-center py-12">
                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <h3 className="mt-2 text-lg font-medium text-gray-900">Nenhum jogador encontrado</h3>
                    <p className="mt-1 text-gray-500">Tente ajustar sua busca ou filtros.</p>
                  </div>
                )}
                
                {filteredPlayers.length > 0 && filteredPlayers.length < players.length && (
                  <div className="mt-8 text-center">
                    <button 
                      onClick={() => {setSearchTerm(''); setFilter('all');}}
                      className="inline-flex items-center text-blue-600 hover:text-blue-800"
                    >
                      <svg className="h-5 w-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                      </svg>
                      Limpar filtros
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}

export default TennisPlayers;

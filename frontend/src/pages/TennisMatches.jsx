import React, { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { Link } from 'react-router-dom'
import api from '../services/api'

const TennisMatches = () => {
  const [filter, setFilter] = useState('upcoming');
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        setLoading(true);
        const response = await api.get('/matches'); // Ajuste do endpoint
        const processedData = response.data.map(match => ({
          ...match,
          player1: match.player1 || { name: "Desconhecido" },
          player2: match.player2 || { name: "Desconhecido" },
          winner: match.winner || { name: "Desconhecido" },
          tournament: match.tournament || { name: "Torneio não informado" },
          date: match.date || "Data não informada",
          score: match.score || "Placar não informado"
        }));
        setMatches(processedData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching matches data:', err);
        setError('Failed to load matches data. Please try again later.');
        setLoading(false);
      }
    };

    fetchMatches();
  }, []);

  // Format the date string to a readable format
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    } catch (e) {
      return dateString; // Return original string if parsing fails
    }
  };

  // Para fins de demonstração, vamos simular partidas futuras e completas
  // Em um ambiente real, isso viria do backend com filtros apropriados
  const upcomingMatches = matches.filter((match, index) => index % 3 === 0);
  const completedMatches = matches.filter((match, index) => index % 3 !== 0);

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="bg-blue-700 text-white py-14 relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-3xl">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Partidas de Tênis</h1>
              <p className="text-xl text-blue-100 mb-6">
                Acompanhe as partidas em andamento, resultados e próximos jogos dos principais torneios de tênis.
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
              src="https://images.unsplash.com/photo-1573680156791-3fe8f2b7b91c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
              alt="Tennis match" 
              className="w-full h-full object-cover object-center"
            />
          </div>
        </section>

        {/* Filter Section */}
        <section className="py-8 bg-white shadow-md">
          <div className="container mx-auto px-4">
            <div className="flex flex-wrap justify-center gap-4">
              <button 
                onClick={() => setFilter('upcoming')}
                className={`py-2 px-6 rounded-lg font-medium ${
                  filter === 'upcoming' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Próximas Partidas
              </button>
              <button 
                onClick={() => setFilter('completed')}
                className={`py-2 px-6 rounded-lg font-medium ${
                  filter === 'completed' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Partidas Concluídas
              </button>
              <button 
                onClick={() => setFilter('live')}
                className={`py-2 px-6 rounded-lg font-medium ${
                  filter === 'live' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                <span className="flex items-center">
                  <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2 animate-pulse"></span>
                  Ao Vivo
                </span>
              </button>
            </div>
          </div>
        </section>

        {/* Matches Section */}
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
                {filter === 'upcoming' && (
                  <>
                    <h2 className="text-2xl font-bold text-blue-900 mb-6">Próximas Partidas</h2>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {upcomingMatches.length > 0 ? upcomingMatches.map((match) => (
                        <div key={match.id} className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow border border-gray-100">
                          <div className="p-4 bg-blue-50 border-b border-blue-100">
                            <div className="flex justify-between items-center">
                              <div>
                                <span className="text-blue-800 font-semibold">{match.tournament.name}</span>
                                <span className="mx-2 text-gray-400">•</span>
                                <span className="text-gray-600">{match.round}</span>
                              </div>
                              <div className="flex items-center text-gray-600 text-sm">
                                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                                {formatDate(match.date)}
                              </div>
                            </div>
                          </div>
                          
                          <div className="p-6">
                            <div className="flex items-center justify-between mb-6">
                              <div className="flex items-center">
                                <div className="w-12 h-12 rounded-full overflow-hidden mr-3 bg-gray-200">
                                  <img 
                                    src={`https://ui-avatars.com/api/?name=${encodeURIComponent(match.player1.name)}&background=0D8ABC&color=fff&size=256`} 
                                    alt={match.player1.name}
                                    className="w-full h-full object-cover" 
                                  />
                                </div>
                                <span className="font-medium text-lg">
                                  {match.player1.name}
                                </span>
                              </div>
                              <div className="text-center">
                                <span className="text-xs text-gray-500 block mb-1">VS</span>
                              </div>
                              <div className="flex items-center">
                                <span className="font-medium text-lg">
                                  {match.player2.name}
                                </span>
                                <div className="w-12 h-12 rounded-full overflow-hidden ml-3 bg-gray-200">
                                  <img 
                                    src={`https://ui-avatars.com/api/?name=${encodeURIComponent(match.player2.name)}&background=0D8ABC&color=fff&size=256`} 
                                    alt={match.player2.name}
                                    className="w-full h-full object-cover" 
                                  />
                                </div>
                              </div>
                            </div>
                            
                            <Link to={`/tennis/matches/${match.id}`} className="w-full block text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                              Ver Detalhes
                            </Link>
                          </div>
                        </div>
                      )) : (
                        <div className="col-span-2 text-center py-12">
                          <p className="text-gray-500">Não há próximas partidas agendadas no momento.</p>
                        </div>
                      )}
                    </div>
                  </>
                )}
                
                {filter === 'completed' && (
                  <>
                    <h2 className="text-2xl font-bold text-blue-900 mb-6">Partidas Concluídas</h2>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {completedMatches.length > 0 ? completedMatches.map((match) => (
                        <div key={match.id} className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow border border-gray-100">
                          <div className="p-4 bg-blue-50 border-b border-blue-100">
                            <div className="flex justify-between items-center">
                              <div>
                                <span className="text-blue-800 font-semibold">{match.tournament.name}</span>
                                <span className="mx-2 text-gray-400">•</span>
                                <span className="text-gray-600">{match.round}</span>
                              </div>
                              <div className="flex items-center text-gray-600 text-sm">
                                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                                {formatDate(match.date)}
                              </div>
                            </div>
                          </div>
                          
                          <div className="p-6">
                            <div className="flex items-center justify-between mb-6">
                              <div className="flex items-center">
                                <div className="w-12 h-12 rounded-full overflow-hidden mr-3 bg-gray-200">
                                  <img 
                                    src={`https://ui-avatars.com/api/?name=${encodeURIComponent(match.player1.name)}&background=0D8ABC&color=fff&size=256`} 
                                    alt={match.player1.name}
                                    className="w-full h-full object-cover" 
                                  />
                                </div>
                                <span className={`font-medium text-lg ${match.winner.id === match.player1.id ? 'font-bold' : ''}`}>
                                  {match.player1.name}
                                  {match.winner.id === match.player1.id && (
                                    <svg className="w-4 h-4 ml-1 inline-block text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                  )}
                                </span>
                              </div>
                              <div className="text-center">
                                <span className="text-sm font-semibold text-gray-800 block">{match.score || "Sem placar"}</span>
                              </div>
                              <div className="flex items-center">
                                <span className={`font-medium text-lg ${match.winner.id === match.player2.id ? 'font-bold' : ''}`}>
                                  {match.player2.name}
                                  {match.winner.id === match.player2.id && (
                                    <svg className="w-4 h-4 ml-1 inline-block text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                  )}
                                </span>
                                <div className="w-12 h-12 rounded-full overflow-hidden ml-3 bg-gray-200">
                                  <img 
                                    src={`https://ui-avatars.com/api/?name=${encodeURIComponent(match.player2.name)}&background=0D8ABC&color=fff&size=256`}
                                    alt={match.player2.name}
                                    className="w-full h-full object-cover" 
                                  />
                                </div>
                              </div>
                            </div>
                            
                            <Link to={`/tennis/matches/${match.id}`} className="w-full block text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                              Ver Resumo
                            </Link>
                          </div>
                        </div>
                      )) : (
                        <div className="col-span-2 text-center py-12">
                          <p className="text-gray-500">Não há partidas concluídas disponíveis.</p>
                        </div>
                      )}
                    </div>
                  </>
                )}
                
                {filter === 'live' && (
                  <div className="flex flex-col items-center justify-center py-12">
                    <svg className="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <h3 className="text-xl font-medium text-gray-900 mb-2">Não há partidas ao vivo no momento</h3>
                    <p className="text-gray-600 mb-6">Verifique novamente mais tarde ou consulte a agenda de próximas partidas.</p>
                    <button 
                      onClick={() => setFilter('upcoming')}
                      className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                    >
                      Ver Próximas Partidas
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

export default TennisMatches;

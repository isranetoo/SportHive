import React, { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { Link } from 'react-router-dom'
import api from '../services/api'

const TennisTournaments = () => {
  const [tournaments, setTournaments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTournaments = async () => {
      try {
        setLoading(true);
        const response = await api.get('/api/tennis/tournaments');
        setTournaments(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching tournaments data:', err);
        setError('Failed to load tournaments data. Please try again later.');
        setLoading(false);
      }
    };

    fetchTournaments();
  }, []);

  // Dividir torneios entre próximos e passados (exemplo simples - em produção deve-se verificar as datas)
  const upcomingTournaments = tournaments.slice(0, Math.ceil(tournaments.length / 2));
  const pastTournaments = tournaments.slice(Math.ceil(tournaments.length / 2));

  // Helper para determinar a cor da superfície
  const getSurfaceColorClass = (surface) => {
    if (!surface) return "bg-gray-100 text-gray-800";
    
    const surfaceLower = surface.toLowerCase();
    if (surfaceLower.includes('grass')) return "bg-green-100 text-green-800";
    if (surfaceLower.includes('clay')) return "bg-orange-100 text-orange-800";
    if (surfaceLower.includes('hard')) return "bg-blue-100 text-blue-800";
    if (surfaceLower.includes('carpet')) return "bg-purple-100 text-purple-800";
    
    return "bg-gray-100 text-gray-800";
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="bg-blue-700 text-white py-14 relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-3xl">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Torneios de Tênis</h1>
              <p className="text-xl text-blue-100 mb-6">
                Confira os principais torneios de tênis ao redor do mundo, suas datas e resultados.
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
              src="https://images.unsplash.com/photo-1610052716767-575595429dc1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
              alt="Tennis court" 
              className="w-full h-full object-cover object-center"
            />
          </div>
        </section>

        {/* Tournaments Sections */}
        <section className="py-12">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-blue-900 mb-8">Torneios</h2>
            
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
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {tournaments.map((tournament) => (
                  <div key={tournament.id} className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow">
                    <div className="h-48 overflow-hidden bg-gray-200">
                      <img 
                        src={tournament.imgUrl || `https://source.unsplash.com/featured/?tennis,${tournament.name}`} 
                        alt={tournament.name} 
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = 'https://images.unsplash.com/photo-1610052716767-575595429dc1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80';
                        }}
                      />
                    </div>
                    <div className="p-6">
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="text-xl font-semibold text-blue-900">{tournament.name}</h3>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSurfaceColorClass(tournament.surface)}`}>
                          {tournament.surface || "Indefinido"}
                        </span>
                      </div>
                      
                      <div className="space-y-2 mb-4">
                        {tournament.location && (
                          <div className="flex items-center text-gray-600">
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                            <span>{tournament.location}</span>
                          </div>
                        )}
                        
                        {tournament.date && (
                          <div className="flex items-center text-gray-600">
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                            </svg>
                            <span>{tournament.date}</span>
                          </div>
                        )}
                        
                        {tournament.prize && (
                          <div className="flex items-center text-gray-600">
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span>{tournament.prize}</span>
                          </div>
                        )}
                        
                        {tournament.series && (
                          <div className="flex items-center text-gray-600">
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"></path>
                            </svg>
                            <span>{tournament.series}</span>
                          </div>
                        )}
                      </div>
                      
                      <Link to={`/tennis/tournaments/${tournament.id}`} className="w-full block text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                        Ver Detalhes
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}

export default TennisTournaments;

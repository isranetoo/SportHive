import React from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

const Tennis = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="flex-grow">
        {/* Hero Section for Tennis */}
        <section className="bg-blue-600 text-white py-20 relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-3xl">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Tênis</h1>
              <p className="text-xl text-blue-100 mb-8">
                Um esporte de raquete que combina elegância, estratégia e potência em quadras de diversos tipos ao redor do mundo.
              </p>
              <button className="bg-white text-blue-600 hover:bg-blue-50 py-3 px-6 rounded-lg font-medium transition-colors">
                Explorar Torneios
              </button>
            </div>
          </div>
          <div className="absolute right-0 bottom-0 w-1/3 h-full opacity-10">
            <img 
              src="https://images.unsplash.com/photo-1531315630201-bb15abeb1653?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" 
              alt="Tennis player silhouette" 
              className="w-full h-full object-cover object-center"
            />
          </div>
        </section>

        {/* Overview Section */}
        <section className="py-16">
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row gap-10">
              <div className="md:w-1/2">
                <h2 className="text-3xl font-bold text-blue-900 mb-6">Sobre o Tênis</h2>
                <p className="text-gray-700 mb-4">
                  O tênis é um esporte praticado entre dois oponentes (simples) ou duas duplas (duplas) em uma quadra dividida por uma rede. 
                  Os jogadores usam uma raquete para rebater uma bola de borracha coberta com feltro.
                </p>
                <p className="text-gray-700 mb-4">
                  O objetivo é rebater a bola de forma que o adversário não consiga devolvê-la corretamente, 
                  conquistando pontos para vencer sets e, consequentemente, a partida.
                </p>
                <p className="text-gray-700">
                  O tênis é um dos esportes mais populares do mundo, com torneios prestigiosos como Grand Slams: 
                  Australian Open, Roland Garros, Wimbledon e US Open.
                </p>
              </div>
              <div className="md:w-1/2 bg-white p-6 rounded-xl shadow-md">
                <h3 className="text-2xl font-semibold text-blue-800 mb-4">Equipamentos Básicos</h3>
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <svg className="w-6 h-6 text-blue-600 mr-2 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    <div>
                      <span className="font-medium">Raquete:</span> Ferramenta principal para golpear a bola, disponível em diversos tamanhos e pesos.
                    </div>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-6 h-6 text-blue-600 mr-2 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    <div>
                      <span className="font-medium">Bolas:</span> Esferas de borracha cobertas de feltro, geralmente amarelas para melhor visibilidade.
                    </div>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-6 h-6 text-blue-600 mr-2 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    <div>
                      <span className="font-medium">Calçados específicos:</span> Tênis projetados para cada tipo de quadra, proporcionando estabilidade e tração.
                    </div>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-6 h-6 text-blue-600 mr-2 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    <div>
                      <span className="font-medium">Vestuário:</span> Roupas leves e confortáveis que permitem ampla movimentação.
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Famous Players Section */}
        <section className="py-16 bg-gray-100">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-blue-900 mb-2 text-center">Grandes Nomes do Tênis</h2>
            <div className="w-20 h-1 bg-blue-600 rounded-full mx-auto mb-10"></div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Roger Federer */}
              <div className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow">
                <div className="h-52 overflow-hidden">
                  <img 
                    src="https://images.unsplash.com/photo-1567081569248-8c272c760a14?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80" 
                    alt="Roger Federer" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-xl font-semibold text-blue-900">Roger Federer</h3>
                  <p className="text-gray-600 mb-3">Suíça</p>
                  <p className="text-gray-700">20 títulos de Grand Slam, considerado um dos mais elegantes tenistas de todos os tempos.</p>
                </div>
              </div>
              
              {/* Rafael Nadal */}
              <div className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow">
                <div className="h-52 overflow-hidden">
                  <img 
                    src="https://images.unsplash.com/photo-1623894433766-caf560095eea?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80" 
                    alt="Rafael Nadal" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-xl font-semibold text-blue-900">Rafael Nadal</h3>
                  <p className="text-gray-600 mb-3">Espanha</p>
                  <p className="text-gray-700">22 títulos de Grand Slam, dominante no saibro com 14 títulos em Roland Garros.</p>
                </div>
              </div>
              
              {/* Serena Williams */}
              <div className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow">
                <div className="h-52 overflow-hidden">
                  <img 
                    src="https://images.unsplash.com/photo-1574812369633-6ee8483de87c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80" 
                    alt="Serena Williams" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-xl font-semibold text-blue-900">Serena Williams</h3>
                  <p className="text-gray-600 mb-3">Estados Unidos</p>
                  <p className="text-gray-700">23 títulos de Grand Slam em simples, uma das maiores tenistas de todos os tempos.</p>
                </div>
              </div>
              
              {/* Novak Djokovic */}
              <div className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow">
                <div className="h-52 overflow-hidden">
                  <img 
                    src="https://images.unsplash.com/photo-1623894433915-11c8ea6078a5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80" 
                    alt="Novak Djokovic" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-xl font-semibold text-blue-900">Novak Djokovic</h3>
                  <p className="text-gray-600 mb-3">Sérvia</p>
                  <p className="text-gray-700">24 títulos de Grand Slam, recordista em semanas como número 1 do mundo.</p>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Tennis Tournaments */}
        <section className="py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-blue-900 mb-2 text-center">Principais Torneios</h2>
            <div className="w-20 h-1 bg-blue-600 rounded-full mx-auto mb-10"></div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="bg-white rounded-xl p-6 shadow-md border-l-4 border-green-500">
                <h3 className="text-2xl font-semibold text-blue-900 mb-3">Wimbledon</h3>
                <p className="text-gray-700 mb-4">O mais antigo e prestigiado torneio de tênis do mundo, jogado na relva do All England Club em Londres.</p>
                <div className="flex items-center text-gray-600">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>Junho/Julho</span>
                </div>
              </div>
              
              <div className="bg-white rounded-xl p-6 shadow-md border-l-4 border-red-500">
                <h3 className="text-2xl font-semibold text-blue-900 mb-3">Roland Garros</h3>
                <p className="text-gray-700 mb-4">O principal torneio de saibro do mundo, realizado anualmente em Paris, França.</p>
                <div className="flex items-center text-gray-600">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>Maio/Junho</span>
                </div>
              </div>
              
              <div className="bg-white rounded-xl p-6 shadow-md border-l-4 border-blue-500">
                <h3 className="text-2xl font-semibold text-blue-900 mb-3">Australian Open</h3>
                <p className="text-gray-700 mb-4">O primeiro Grand Slam do ano, jogado em quadras duras em Melbourne, Austrália.</p>
                <div className="flex items-center text-gray-600">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>Janeiro</span>
                </div>
              </div>
              
              <div className="bg-white rounded-xl p-6 shadow-md border-l-4 border-yellow-500">
                <h3 className="text-2xl font-semibold text-blue-900 mb-3">US Open</h3>
                <p className="text-gray-700 mb-4">O último Grand Slam do ano, disputado em quadras duras em Nova York, EUA.</p>
                <div className="flex items-center text-gray-600">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>Agosto/Setembro</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}

export default Tennis;

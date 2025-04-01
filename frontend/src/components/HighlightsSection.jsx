import React from 'react';

function HighlightsSection() {
  return (
    <section id="destaques" className="py-16 md:py-20 bg-white relative overflow-hidden w-full">
      <div className="container mx-auto px-4 relative z-10">
        <div className="flex flex-col items-center mb-10">
          <h2 className="text-3xl font-bold text-blue-900 mb-2">Destaques da Semana</h2>
          <div className="w-20 h-1 bg-blue-600 rounded-full"></div>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 md:gap-8">
          <div className="bg-gray-50 p-6 rounded-2xl shadow-md h-full hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold text-blue-600 mb-3">Final do campeonato de futebol</h3>
            <p className="text-gray-600 mb-4">Acompanhe ao vivo a grande final do campeonato nacional.</p>
            <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors w-full">
              Saiba mais
            </button>
          </div>
          <div className="bg-gray-50 p-6 rounded-2xl shadow-md h-full hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold text-blue-600 mb-3">Torneio de tênis</h3>
            <p className="text-gray-600 mb-4">Os melhores tenistas do mundo se encontram no Grand Slam.</p>
            <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors w-full">
              Saiba mais
            </button>
          </div>
          <div className="bg-gray-50 p-6 rounded-2xl shadow-md h-full hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold text-blue-600 mb-3">Playoff de basquete</h3>
            <p className="text-gray-600 mb-4">Não perca nenhum detalhe dos playoffs da temporada.</p>
            <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors w-full">
              Saiba mais
            </button>
          </div>
        </div>
      </div>
      <div className="absolute w-56 h-56 bg-blue-600/10 rounded-full -bottom-20 -left-20 z-0"></div>
      <div className="absolute w-40 h-40 bg-blue-600/10 rounded-full -top-12 -right-12 z-0"></div>
    </section>
  );
}

export default HighlightsSection;

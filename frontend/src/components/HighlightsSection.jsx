import React from 'react';

function HighlightsSection() {
  return (
    <section id="destaques" className="py-16 md:py-20 bg-indigo-50 w-full">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center text-blue-900 mb-8 md:mb-12">Destaques da Semana</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 md:gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md h-full">
            <h3 className="text-xl font-semibold text-blue-900 mb-3">Final do campeonato de futebol</h3>
            <p className="text-gray-600">Acompanhe ao vivo a grande final do campeonato nacional.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md h-full">
            <h3 className="text-xl font-semibold text-blue-900 mb-3">Torneio de tênis</h3>
            <p className="text-gray-600">Os melhores tenistas do mundo se encontram no Grand Slam.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md h-full">
            <h3 className="text-xl font-semibold text-blue-900 mb-3">Playoff de basquete</h3>
            <p className="text-gray-600">Não perca nenhum detalhe dos playoffs da temporada.</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default HighlightsSection;

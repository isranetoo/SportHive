import React from 'react';

function SportsSection({ loading, sports }) {
  return (
    <section id="esportes" className="py-16 md:py-20 w-full">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center text-blue-900 mb-8 md:mb-12">Esportes Disponíveis</h2>
        
        {loading ? (
          <div className="text-center py-10 text-gray-500 text-xl">Carregando esportes...</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8">
            {sports.map(sport => (
              <div key={sport.id} className="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 hover:-translate-y-1 transform h-full flex flex-col">
                <div className="h-40 md:h-48 overflow-hidden">
                  <img src={sport.image} alt={sport.name} className="w-full h-full object-cover transition-transform duration-500 hover:scale-105" />
                </div>
                <div className="p-5 md:p-6 flex-grow flex flex-col">
                  <h3 className="text-xl font-semibold text-blue-900 mb-2">{sport.name}</h3>
                  <p className="text-gray-600 mb-4 flex-grow">{sport.description}</p>
                  <button className="bg-blue-900 hover:bg-blue-800 text-white py-2 px-4 rounded-md font-medium transition-colors w-full">
                    Ver mais
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

export default SportsSection;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SportsSection({ loading, sports }) {
  const navigate = useNavigate();
  const [visibleItems, setVisibleItems] = useState(4);
  
  const loadMore = () => {
    setVisibleItems(prev => prev + 4);
  };

  const handleSportClick = (sportName) => {
    // Traduz os nomes dos esportes e depois converte para minúsculas para o roteamento
    const sportTranslations = {
      "Tênis": "tennis",
      "Futebol": "soccer",
      "Golf": "golf",
      "Vôlei": "volleyball",
      "Xadrez": "chess",
    };
    
    // Verifica se existe tradução, senão usa o original convertido para minúsculas
    const translatedName = sportTranslations[sportName] || sportName.toLowerCase();
    navigate(`/${translatedName}`);
  };

  return (
    <section id="esportes" className="py-16 md:py-20 w-full bg-gray-50 relative overflow-hidden">
      <div className="container mx-auto px-4 relative z-10">
        <div className="flex flex-col items-center mb-10">
          <h2 className="text-3xl font-bold text-blue-900 mb-2">Esportes Disponíveis</h2>
          <div className="w-20 h-1 bg-blue-600 rounded-full"></div>
        </div>
        
        {loading ? (
          <div className="text-center py-10 text-gray-500 text-xl">Carregando esportes...</div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8">
              {sports.slice(0, visibleItems).map(sport => (
                <div key={sport.id} className="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 hover:-translate-y-1 transform h-full flex flex-col">
                  <div className="h-40 md:h-48 overflow-hidden">
                    <img src={sport.image} alt={sport.name} className="w-full h-full object-cover transition-transform duration-500 hover:scale-105" />
                  </div>
                  <div className="p-5 md:p-6 flex-grow flex flex-col">
                    <h3 className="text-xl font-semibold text-blue-900 mb-2">{sport.name}</h3>
                    <p className="text-gray-600 mb-4 flex-grow">{sport.description}</p>
                    <button 
                      className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors w-full"
                      onClick={() => handleSportClick(sport.name)}
                    >
                      Ver mais
                    </button>
                  </div>
                </div>
              ))}
            </div>
            
            {visibleItems < sports.length && (
              <div className="flex justify-center mt-10">
                <button 
                  onClick={loadMore}
                  className="bg-blue-600 hover:bg-blue-700 text-white py-3 px-6 rounded-lg font-medium transition-colors"
                >
                  Ver mais esportes
                </button>
              </div>
            )}
          </>
        )}
      </div>
      <div className="absolute w-56 h-56 bg-blue-600/10 rounded-full -bottom-20 -right-20 z-0"></div>
      <div className="absolute w-40 h-40 bg-blue-600/10 rounded-full -top-12 -left-12 z-0"></div>
    </section>
  );
}

export default SportsSection;

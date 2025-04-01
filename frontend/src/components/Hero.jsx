import React from 'react';

function Hero() {
  return (
    <section 
      className="py-20 md:py-32 bg-gradient-to-br from-blue-900 via-red-700 to-yellow-400 text-white text-center bg-cover bg-center w-full relative" 
    >
      <div className="absolute inset-0 bg-black opacity-60"></div>
      <div className="container mx-auto px-4 relative z-10">
        <div className="flex flex-col items-center mb-6">
          <div className="w-20 h-20 rounded-full bg-blue-600 flex justify-center items-center mb-4">
            <span className="text-white text-3xl font-bold">SH</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-6">Bem-vindo ao SportHive</h2>
          <p className="text-xl max-w-3xl mx-auto mb-8">Acompanhe resultados, estatísticas e notícias de diversos esportes em um só lugar</p>
          <a href="#esportes" className="bg-white text-blue-600 hover:bg-blue-50 py-3 px-6 rounded-lg font-bold transition-colors text-lg">
            Explorar Esportes
          </a>
        </div>
      </div>
      <div className="absolute w-72 h-72 bg-blue-600/20 rounded-full -bottom-40 -right-20 z-0"></div>
      <div className="absolute w-48 h-48 bg-blue-600/20 rounded-full -top-20 -left-20 z-0"></div>
    </section>
  );
}

export default Hero;

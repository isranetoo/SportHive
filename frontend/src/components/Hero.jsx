import React from 'react';

function Hero() {
  return (
    <section 
      className="py-16 md:py-24 bg-gradient-to-r from-blue-900 to-indigo-900 text-white text-center bg-cover bg-center w-full" 
      style={{ 
        backgroundImage: "linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1461896836934-ffe607ba8211?ixlib=rb-4.0.3&auto=format&fit=crop&w=1900&q=80')" 
      }}
    >
      <div className="container mx-auto px-4">
        <h2 className="text-4xl md:text-5xl font-bold mb-6">Bem-vindo ao mundo dos esportes</h2>
        <p className="text-xl max-w-3xl mx-auto">Acompanhe resultados, estatísticas e notícias de diversos esportes em um só lugar</p>
      </div>
    </section>
  );
}

export default Hero;

import React from 'react';

function Navbar() {
  return (
    <header className="bg-blue-900 text-white py-6 w-full">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold mb-1">SportHive</h1>
        <p className="text-blue-100 mb-4">Sua plataforma completa de informações esportivas</p>
        <div className="flex justify-between items-center">
          <nav>
            <ul className="flex flex-wrap gap-6 md:gap-8">
              <li><a href="#home" className="hover:text-blue-200 transition-colors font-medium">Home</a></li>
              <li><a href="#esportes" className="hover:text-blue-200 transition-colors font-medium">Esportes</a></li>
              <li><a href="#noticias" className="hover:text-blue-200 transition-colors font-medium">Notícias</a></li>
              <li><a href="#eventos" className="hover:text-blue-200 transition-colors font-medium">Eventos</a></li>
              <li><a href="#sobre" className="hover:text-blue-200 transition-colors font-medium">Sobre</a></li>
            </ul>
          </nav>
          <div className="flex gap-4">
            <button className="bg-transparent border border-white hover:bg-white hover:text-blue-900 text-white py-2 px-4 rounded-md font-medium transition-colors">
              Entrar
            </button>
            <button className="bg-white text-blue-900 hover:bg-blue-100 py-2 px-4 rounded-md font-medium transition-colors">
              Registrar
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;

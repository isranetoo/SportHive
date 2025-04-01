import React from 'react';

function Navbar() {
  return (
    <header className="bg-blue-600 text-white py-4 w-full shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-10 h-10 rounded-full bg-white flex justify-center items-center mr-3">
              <span className="text-blue-600 text-lg font-bold">SH</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold mb-0">SportHive</h1>
              <p className="text-blue-100 text-xs">Sua plataforma completa de informações esportivas</p>
            </div>
          </div>

          <nav className="hidden md:block">
            <ul className="flex gap-6">
              <li><a href="#home" className="hover:text-blue-200 transition-colors font-medium">Home</a></li>
              <li><a href="#esportes" className="hover:text-blue-200 transition-colors font-medium">Esportes</a></li>
              <li><a href="#noticias" className="hover:text-blue-200 transition-colors font-medium">Notícias</a></li>
              <li><a href="#eventos" className="hover:text-blue-200 transition-colors font-medium">Eventos</a></li>
              <li><a href="#sobre" className="hover:text-blue-200 transition-colors font-medium">Sobre</a></li>
            </ul>
          </nav>
          
          <div className="flex gap-3">
            <a href="/login" className="bg-transparent border border-white hover:bg-white hover:text-blue-600 text-white py-2 px-4 rounded-lg font-medium transition-colors">
              Entrar
            </a>
            <a href="/register" className="bg-white text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg font-medium transition-colors">
              Registrar
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;

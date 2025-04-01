import React from 'react';

function Footer() {
  return (
    <footer className="bg-blue-600 text-white py-8 w-full mt-auto relative overflow-hidden">
      <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4 relative z-10">
        <div className="flex items-center mb-4 md:mb-0">
          <div className="w-10 h-10 rounded-full bg-white flex justify-center items-center mr-3">
            <span className="text-blue-600 text-sm font-bold">SH</span>
          </div>
          <p>&copy; 2025 SportHive - Todos os direitos reservados</p>
        </div>
        <div className="flex gap-6">
          <a href="#termos" className="text-white hover:text-blue-100 transition-colors">Termos de Uso</a>
          <a href="#privacidade" className="text-white hover:text-blue-100 transition-colors">Política de Privacidade</a>
          <a href="#contato" className="text-white hover:text-blue-100 transition-colors">Contato</a>
        </div>
      </div>
      <div className="absolute w-40 h-40 bg-blue-700/50 rounded-full -top-20 -right-20 z-0"></div>
      <div className="absolute w-24 h-24 bg-blue-700/50 rounded-full -bottom-10 -left-10 z-0"></div>
    </footer>
  );
}

export default Footer;

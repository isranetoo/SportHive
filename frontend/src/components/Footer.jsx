import React from 'react';

function Footer() {
  return (
    <footer className="bg-blue-900 text-white py-6 md:py-8 w-full mt-auto">
      <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
        <p>&copy; 2025 SportHive - Todos os direitos reservados</p>
        <div className="flex gap-6">
          <a href="#termos" className="text-blue-100 hover:text-white transition-colors">Termos de Uso</a>
          <a href="#privacidade" className="text-blue-100 hover:text-white transition-colors">Política de Privacidade</a>
          <a href="#contato" className="text-blue-100 hover:text-white transition-colors">Contato</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;

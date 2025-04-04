import React, { useState, useEffect, useRef } from 'react';
import { isLoggedIn, getCurrentUser, logout } from '../services/auth';

function Navbar() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  
  // Função para buscar dados do usuário
  const fetchUserData = async () => {
    if (isLoggedIn()) {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error("Erro ao buscar dados do usuário:", error);
        setUser(null);
      }
    } else {
      setUser(null);
    }
    setLoading(false);
  };
  
  useEffect(() => {
    fetchUserData();
    
    // Verificar status de login sempre que o componente for montado
    const checkLoginStatus = () => {
      if (!isLoggedIn()) {
        setUser(null);
      }
    };
    
    window.addEventListener('storage', checkLoginStatus);
    return () => {
      window.removeEventListener('storage', checkLoginStatus);
    };
  }, []);
  
  // Fecha o dropdown quando clica fora dele
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    }
    
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownRef]);
  
  // Função de logout aprimorada
  const handleLogout = (e) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    
    // Executar logout
    logout();
    
    // Atualizar estado do componente
    setUser(null);
    setDropdownOpen(false);
    
    // Forçar recarregamento da página para garantir que todos os estados sejam resetados
    window.location.href = '/';
  };
  
  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

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
          
          <div className="flex gap-3 items-center">
            {!loading && (
              user ? (
                <div className="flex items-center relative" ref={dropdownRef}>
                  <div className="mr-4 text-right cursor-pointer" onClick={toggleDropdown}>
                    <div className="flex items-center">
                      <div>
                        <p className="font-medium">{user.name}</p>
                        <p className="text-xs text-blue-100">{user.email}</p>
                      </div>
                      <svg 
                        className={`ml-2 w-4 h-4 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} 
                        fill="none" 
                        stroke="currentColor" 
                        viewBox="0 0 24 24" 
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                      </svg>
                    </div>
                  </div>
                  
                  {/* Dropdown Menu */}
                  {dropdownOpen && (
                    <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg z-10 py-2">
                      <a href="/profile" className="block px-4 py-2 text-blue-600 hover:bg-blue-50 transition-colors">
                        <div className="flex items-center">
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                          </svg>
                          Perfil
                        </div>
                      </a>
                      <a href="/partidas" className="block px-4 py-2 text-blue-600 hover:bg-blue-50 transition-colors">
                        <div className="flex items-center">
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                          </svg>
                          Partidas
                        </div>
                      </a>
                      <a href="/opcoes" className="block px-4 py-2 text-blue-600 hover:bg-blue-50 transition-colors">
                        <div className="flex items-center">
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                          </svg>
                          Opções
                        </div>
                      </a>
                      <div className="border-t border-gray-200 my-1"></div>
                      <button 
                        type="button"
                        onClick={handleLogout}
                        className="w-full text-left px-4 py-2 hover:bg-blue-50 transition-colors text-red-600"
                      >
                        <div className="flex items-center">
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                          </svg>
                          Sair
                        </div>
                      </button>
                    </div>
                  )}
                  
                </div>
              ) : (
                <>
                  <a href="/login" className="bg-transparent border border-white hover:bg-white hover:text-blue-600 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                    Entrar
                  </a>
                  <a href="/register" className="bg-white text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg font-medium transition-colors">
                    Registrar
                  </a>
                </>
              )
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;

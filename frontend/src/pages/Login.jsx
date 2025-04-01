import { useState } from "react";
import { loginUser } from "../services/auth";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        
        try {
            await loginUser(email, password);
            window.location.href = "/profile";
        } catch (error) {
            setError("Credenciais inválidas. Tente novamente.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-900 via-red-700 to-yellow-400 p-5 font-sans">
            <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 relative overflow-hidden">
                <div className="flex flex-col items-center mb-6">
                    <div className="w-16 h-16 rounded-full bg-blue-600 flex justify-center items-center mb-3">
                        <span className="text-white text-2xl font-bold">SH</span>
                    </div>
                    <h1 className="text-3xl font-bold text-gray-800 m-0">SportHive</h1>
                    <p className="text-sm text-gray-500 mt-1">Entre para acessar sua conta</p>
                </div>
                
                {error && (
                    <div className="bg-red-100 text-red-700 p-3 rounded-lg mb-4 text-center text-sm">
                        {error}
                    </div>
                )}
                
                <form onSubmit={handleLogin} className="flex flex-col gap-5">
                    <div className="flex flex-col gap-1">
                        <label className="text-sm font-bold text-gray-600">E-mail</label>
                        <input 
                            type="email" 
                            placeholder="seu@email.com" 
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)} 
                            className="py-3 px-4 rounded-lg border border-gray-300 text-base focus:border-blue-600 focus:outline-none"
                            required
                        />
                    </div>
                    
                    <div className="flex flex-col gap-1">
                        <label className="text-sm font-bold text-gray-600">Senha</label>
                        <input 
                            type="password" 
                            placeholder="Sua senha" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            className="py-3 px-4 rounded-lg border border-gray-300 text-base focus:border-blue-600 focus:outline-none"
                            required
                        />
                    </div>
                    
                    <div className="text-right text-sm -mt-2">
                        <a href="#" className="text-blue-600 font-bold hover:underline">Esqueceu a senha?</a>
                    </div>
                    
                    <button 
                        type="submit" 
                        className={`bg-blue-600 text-white border-0 rounded-lg py-3 text-base font-bold cursor-pointer transition-colors ${loading ? 'opacity-70' : 'hover:bg-blue-700'}`}
                        disabled={loading}
                    >
                        {loading ? "Entrando..." : "Entrar"}
                    </button>
                </form>
                
                <div className="mt-6 text-center">
                    <p className="text-sm text-gray-500">
                        Não tem uma conta? <a href="/register" className="text-blue-600 font-bold hover:underline">Registre-se</a>
                    </p>
                </div>
                
                <div className="absolute w-40 h-40 bg-blue-600/10 rounded-full -bottom-20 -right-20 z-0"></div>
                <div className="absolute w-24 h-24 bg-blue-600/10 rounded-full -top-12 -left-12 z-0"></div>
            </div>
        </div>
    );
}

export default Login;

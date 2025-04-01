import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/auth";

function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const validateForm = () => {
        if (!name || !email || !password || !confirmPassword) {
            setError("Todos os campos são obrigatórios");
            return false;
        }
        
        if (password !== confirmPassword) {
            setError("As senhas não coincidem");
            return false;
        }
        
        if (password.length < 6) {
            setError("A senha deve ter pelo menos 6 caracteres");
            return false;
        }
        
        return true;
    };

    const handleSignUp = async (e) => {
        e.preventDefault();
        setError("");
        
        if (!validateForm()) return;
        
        setLoading(true);
        
        try {
            // Using the registerUser function from auth service
            await registerUser(name, email, password);
            
            // Redirecionar para login após cadastro
            navigate("/login");
        } catch (error) {
            setError("Erro ao criar conta. Tente novamente.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-900 via-red-700 to-yellow-400 p-5 font-sans">
            <div className="w-full max-w-lg bg-white rounded-2xl shadow-lg p-8 relative overflow-hidden">
                <div className="flex flex-col items-center mb-6">
                    <div className="w-16 h-16 rounded-full bg-blue-600 flex justify-center items-center mb-3">
                        <span className="text-white text-2xl font-bold">SH</span>
                    </div>
                    <h1 className="text-3xl font-bold text-gray-800 m-0">SportHive</h1>
                    <p className="text-sm text-gray-500 mt-1">Crie sua conta e comece a jornada</p>
                </div>
                
                {error && (
                    <div className="bg-red-100 text-red-700 p-3 rounded-lg mb-4 text-center text-sm">
                        {error}
                    </div>
                )}
                
                <form onSubmit={handleSignUp} className="flex flex-col gap-5">
                    <div className="flex flex-col gap-1">
                        <label className="text-sm font-bold text-gray-600">Nome completo</label>
                        <input 
                            type="text" 
                            placeholder="Seu nome" 
                            value={name} 
                            onChange={(e) => setName(e.target.value)} 
                            className="py-3 px-4 rounded-lg border border-gray-300 text-base focus:border-blue-600 focus:outline-none"
                            required
                        />
                    </div>
                    
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
                            placeholder="Crie uma senha forte" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            className="py-3 px-4 rounded-lg border border-gray-300 text-base focus:border-blue-600 focus:outline-none"
                            required
                        />
                    </div>
                    
                    <div className="flex flex-col gap-1">
                        <label className="text-sm font-bold text-gray-600">Confirme sua senha</label>
                        <input 
                            type="password" 
                            placeholder="Digite a senha novamente" 
                            value={confirmPassword} 
                            onChange={(e) => setConfirmPassword(e.target.value)} 
                            className="py-3 px-4 rounded-lg border border-gray-300 text-base focus:border-blue-600 focus:outline-none"
                            required
                        />
                    </div>
                    
                    <button 
                        type="submit" 
                        className={`bg-blue-600 text-white border-0 rounded-lg py-3 mt-3 text-base font-bold cursor-pointer transition-colors ${loading ? 'opacity-70' : 'hover:bg-blue-700'}`}
                        disabled={loading}
                    >
                        {loading ? "Criando conta..." : "Criar conta"}
                    </button>
                </form>
                
                <div className="mt-6 text-center">
                    <p className="text-sm text-gray-500">
                        Já tem uma conta? <a href="/login" className="text-blue-600 font-bold hover:underline">Entrar</a>
                    </p>
                </div>
                
                <div className="absolute w-40 h-40 bg-blue-600/10 rounded-full -bottom-20 -right-20 z-0"></div>
                <div className="absolute w-24 h-24 bg-blue-600/10 rounded-full -top-12 -left-12 z-0"></div>
            </div>
        </div>
    );
}

export default Register;

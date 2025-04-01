import { useEffect, useState } from "react";
import { getProfile } from "../services/auth";

function Profile() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        getProfile()
            .then(response => setUser(response.data))
            .catch(() => {
                window.location.href = "/login";
            });
    }, []);

    return (
        <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-900 via-red-700 to-yellow-400 p-5 font-sans">
            <div className="w-full max-w-lg bg-white rounded-2xl shadow-lg p-8 relative overflow-hidden">
                <div className="flex flex-col items-center mb-6">
                    <div className="w-16 h-16 rounded-full bg-blue-600 flex justify-center items-center mb-3">
                        <span className="text-white text-2xl font-bold">SH</span>
                    </div>
                    <h1 className="text-3xl font-bold text-gray-800 m-0">Perfil</h1>
                    <p className="text-sm text-gray-500 mt-1">Bem-vindo ao seu perfil</p>
                </div>

                {user ? (
                    <div className="text-center">
                        <h2 className="text-xl font-bold text-blue-900 mb-4">Olá, {user.name}!</h2>
                        <p className="text-gray-600 mb-4">E-mail: {user.email}</p>
                        <button
                            onClick={() => (window.location.href = "/")}
                            className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
                        >
                            Voltar para Home
                        </button>
                    </div>
                ) : (
                    <div className="text-center py-10 text-gray-500 text-xl">Carregando...</div>
                )}

                <div className="absolute w-40 h-40 bg-blue-600/10 rounded-full -bottom-20 -right-20 z-0"></div>
                <div className="absolute w-24 h-24 bg-blue-600/10 rounded-full -top-12 -left-12 z-0"></div>
            </div>
        </div>
    );
}

export default Profile;

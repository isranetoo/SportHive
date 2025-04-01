import { useEffect, useState } from "react";
import { getProfile } from "../services/auth";

function Profile() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        getProfile().then(response => setUser(response.data)).catch(() => {
            alert("Faça login primeiro!");
            window.location.href = "/login";
        });
    }, []);

    return user ? <h1>Bem-vindo, {user.name}!</h1> : <p>Carregando...</p>;
}

export default Profile;

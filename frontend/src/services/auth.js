import axios from "axios";

const API_URL = "http://localhost:8000/";

export const registerUser = async (name, email, password) => {
    try {
        const response = await axios.post("http://localhost:8000/register", {
            name,
            email,
            password,
        });

        return response.data;
    } catch (error) {
        console.error("Erro ao registrar usuário:", error.response?.data || error.message);
        throw error;
    }
};

export const loginUser = async (email, password) => {
    const response = await axios.post(`${API_URL}login`, { email, password });
    localStorage.setItem("token", response.data.access_token);
};

export const getProfile = async () => {
    const token = localStorage.getItem("token");
    return axios.get(`${API_URL}profile`, {
        headers: { Authorization: `Bearer ${token}` }
    });
};

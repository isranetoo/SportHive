import axios from "axios";

const API_URL = "http://localhost:5173/";

export const registerUser = async (name, email, password) => {
    return axios.post(`${API_URL}register`, { name, email, password });
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

import axios from "axios";

const API_URL = "http://localhost:8000/api/";

// Helper function to parse database schema errors
const parseDbSchemaError = (errorDetail) => {
    if (errorDetail && errorDetail.includes("column") && errorDetail.includes("does not exist")) {
        return {
            isDatabaseSchemaError: true,
            userMessage: "Erro de configuração do sistema. Por favor, contate o suporte.",
            developerMessage: errorDetail
        };
    }
    return null;
};

export const registerUser = async (name, email, password) => {
    try {
        const response = await axios.post(`${API_URL}register`, {
            name,
            email,
            password,
        });

        return response.data;
    } catch (error) {
        const errorDetail = error.response?.data?.detail || error.message;
        console.error("Erro ao registrar usuário:", errorDetail);
        
        // Check if it's a database schema error
        const schemaError = parseDbSchemaError(errorDetail);
        if (schemaError) {
            throw schemaError;
        }
        
        throw { message: errorDetail };
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

import { useEffect, useState } from "react";
import { fetchData } from "./services/api";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Hero from "./components/Hero";
import SportsSection from "./components/SportsSection";
import HighlightsSection from "./components/HighlightsSection";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";

function App() {
    const [loading, setLoading] = useState(true);
    const [sports, setSports] = useState([]);

    useEffect(() => {
        const loadData = async () => {
            try {
                const data = await fetchData();
                if (data) {
                    setSports(data);
                }
                setLoading(false);
            } catch (error) {
                console.error("Erro ao carregar dados:", error);
                setLoading(false);
            }
        };
        
        loadData();
    }, []);

    const HomePage = () => (
        <div className="flex flex-col min-h-screen w-full bg-gray-50">
            <Navbar />
            <main className="flex-grow w-full">
                <Hero />
                <SportsSection loading={loading} sports={sports} />
                <HighlightsSection />
            </main>
            <Footer />
        </div>
    );

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/profile" element={<Profile />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;

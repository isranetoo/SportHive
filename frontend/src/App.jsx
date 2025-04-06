import { useEffect, useState } from "react";
import { fetchData } from "./services/api";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Hero from "./components/Hero";
import SportsSection from "./components/SportsSection";
import HighlightsSection from "./components/HighlightsSection";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Tennis from "./pages/Tennis";
import TennisRanking from "./pages/TennisRanking";
import TennisTournaments from "./pages/TennisTournaments";
import TennisPlayers from "./pages/TennisPlayers";
import TennisHeadToHead from "./pages/TennisHeadToHead";
import TennisMatches from "./pages/TennisMatches";

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
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/tennis" element={<Tennis />} />
                <Route path="/tennis/ranking" element={<TennisRanking />} />
                <Route path="/tennis/tournaments" element={<TennisTournaments />} />
                <Route path="/tennis/players" element={<TennisPlayers />} />
                <Route path="/tennis/head-to-head" element={<TennisHeadToHead />} />
                <Route path="/tennis/matches" element={<TennisMatches />} />
                <Route path="*" element={<div>Page not found</div>} />
            </Routes>
        </Router>
    );
}

export default App;

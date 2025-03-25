import { useEffect, useState } from "react";
import { fetchData } from "./services/api";

function App() {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetchData().then((result) => setData(result));
    }, []);

    return (
        <div>
            <h1>Dados do Backend</h1>
            {data ? (
                <div>
                    <p>{data.message}</p>
                    <ul>
                        {data.items.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>Carregando...</p>
            )}
        </div>
    );
}

export default App;

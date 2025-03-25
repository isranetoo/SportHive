import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir que o frontend (React) acesse o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para o domínio do seu frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para carregar dados do arquivo JSON
def load_sports_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "data", "sports.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Erro ao carregar arquivo JSON: {e}")
        # Retorna dados padrão caso haja erro na leitura do arquivo
        return []

# Rota para enviar dados ao React
@app.get("/api/dataset")
def get_data():
    return load_sports_data()

# Rodar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

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

# Rota para enviar dados ao React
@app.get("/api/dataset")
def get_data():
    return {"message": "Olá, React!", "items": ["Israel", 2, 3, 4, 5]}

# Rodar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

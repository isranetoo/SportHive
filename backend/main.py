from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import Sport, User
from auth import router as auth_router  # Importando as rotas de auth.py
from profile import router as profile_router  # Importando as rotas de profile.py

app = FastAPI()

origins = [
    "http://localhost:5173",  # Frontend local
    "https://seu-dominio.com"  # 🔴 Adicione o domínio em produção
]

# Permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para buscar os esportes do banco de dados
@app.get("/api/dataset")
def get_data(db: Session = Depends(get_db)):
    sports = db.query(Sport).all()
    return [{"id": s.id, "name": s.name, "category": s.category} for s in sports]

# Include routers
app.include_router(auth_router)
app.include_router(profile_router)

@app.get("/")
def home():
    return {"message": "API está funcionando!"}

# Rodar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

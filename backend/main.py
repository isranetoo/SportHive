from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Sport, User
from auth import router as auth_router  # Importando as rotas de auth.py
from profile import router as profile_router  # Importando as rotas de profile.py
from tennis_routes import router as tennis_router, add_cors_middleware  # Importando as rotas de tênis
import os

# Inicializa o banco de dados
init_db()

app = FastAPI()

# Add CORS middleware
add_cors_middleware(app)

# Rota para buscar os esportes do banco de dados
@app.get("/api/dataset")
def get_data(db: Session = Depends(get_db)):
    sports = db.query(Sport).all()
    return [{"id": s.id, "name": s.name, "category": s.category, "description": s.description, "image": s.image} for s in sports]

# Include routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(tennis_router)  # Adiciona as rotas de tênis

@app.get("/")
def home():
    return {"message": "API está funcionando!"}

# Rodar o servidor
if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo usuário.")

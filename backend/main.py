from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import Sport, User
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

origins = [
    "http://localhost:5173",  # Frontend local
    "https://seu-dominio.com"  # 🔴 Adicione o domínio em produção
]

# Permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # Altere para o domínio do seu frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração para hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

@app.post("/api/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Verificar se o email já está cadastrado
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Criar novo usuário com senha hash
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
    )
    db.add(new_user)
    db.commit()

    return {"message": "Usuário registrado com sucesso!"}

# Rota para buscar os esportes do banco de dados
@app.get("/api/dataset")
def get_data(db: Session = Depends(get_db)):
    sports = db.query(Sport).all()
    return [{"id": s.id, "name": s.name, "category": s.category} for s in sports]

# Rodar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

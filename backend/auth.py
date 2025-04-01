from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_db
from models import User
from pydantic import BaseModel

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        # Verifica se o e-mail já existe
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")

        # Cria o novo usuário
        new_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Usuário registrado com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Verifica se o usuário existe no banco
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    # Aqui você geraria o token, mas vamos focar na estrutura inicial
    return {"message": "Login bem-sucedido!"}

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from .data import get_db
from .models import User

router = APIRouter()
SECRET_KEY = "chave-super-segura"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(lambda token: token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/profile")
def get_profile(email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"name": user.name, "email": user.email}

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from database import get_db
from models import User
from sqlalchemy.orm import Session
from auth import get_current_user

router = APIRouter()

@router.get("/api/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {"name": current_user.name, "email": current_user.email}

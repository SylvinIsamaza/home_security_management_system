from fastapi import APIRouter, Depends, HTTPException, status
from ..crud import user 
from ..schemas import UserCreate, User  
from ..database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta 
from typing import List
from ..models import User as DBUser 
from sqlalchemy.orm import Session
from ..crud import  create_user, get_user_by_id, get_users, delete_user,get_user
from ..utils import get_password_hash,verify_password,create_access_token,get_current_user

router = APIRouter()
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(db, username=user.username)  
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = get_password_hash(user.password)
    return create_user(db, user=UserCreate(username=user.username, password=hashed_password))  

@router.get("/me", response_model=User)
def get_current_user_info(current_user: DBUser = Depends(get_current_user)):  



    return current_user

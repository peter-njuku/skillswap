from datetime import datetime,timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..config import settings
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ...app import models
from typing import Optional

SECRET_KEY= settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_EXPIRY_MINUTES=30
auth_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict,expires:Optional[timedelta]=None):
    to_encode=data.copy()

    if expires:
        expire=datetime.utcnow()+expires
    else: 
        expire=datetime.utcnow()+timedelta(minutes=15)
    
    to_encode.update({"exp":expire})

    encode_jwt=jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

async def get_current_user(token: str=Depends(auth_scheme)):
    credential_exceptions=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Credentials",
                header={"WWW-Authenticate":"Bearer"}
            )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credential_exceptions
    except JWTError: 
        raise credential_exceptions
    return {"email":email}
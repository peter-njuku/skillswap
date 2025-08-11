from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session

from ..database import get_db, engine
from ...app import models
from . import schemas
from .auth_utils import get_password_hash, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRY_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])
models.Base.metadata.create_all(bind=engine)

@router.post("/register",response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: session = Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    hashed_password=get_password_hash(user.password)
    new_user=models.User(email=user.email,hashed_password=hashed_password,full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(), db:session=Depends(get_db)):
    user=authenticate_user(db,email=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            headers={"WWW-AUTHENTICATE":"Bearer"})
    token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    access_token=create_access_token(data={"sub":user.email},expires=token_expires)
    return {"access_token":access_token,"token_type":"Bearer"}
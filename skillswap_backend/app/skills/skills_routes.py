from fastapi import APIRouter, Depends, HTTPException
from .. import models
from ..database import db_dependancy
from ..auth.auth_utils import get_current_user
from . import skills_schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=skills_schemas.UserProfileOut)
def get_my_profile(db:db_dependancy, current_user:dict=Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=skills_schemas.UserProfileOut)
def update_my_profile(profile_data:skills_schemas.UserProfileUpdate, db:db_dependancy, current_user:dict=Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email=profile_data.email
    user.bio = profile_data.bio

    skills = db.query(models.Skill).filter(models.Skill.user_id == user.id).delete()
    print("Skills deleted fr update")

    for skill in profile_data.skills:
        new_skill = models.Skill(name=skill.name, type=skill.type, owner=user)
        db.add(new_skill)
    
    db.commit()
    db.refresh(user)
    return user

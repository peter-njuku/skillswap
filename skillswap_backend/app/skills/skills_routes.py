from fastapi import APIRouter, Depends, HTTPException, Query
from .. import models
from ..database import db_dependancy
from ..auth.auth_utils import get_current_user
from . import skills_schemas
from typing import List

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

@router.get("/search", response_model=List[skills_schemas.UserProfileOut])
def search_user_by_skill(db:db_dependancy, 
                         current_user:dict=Depends(get_current_user),
                         name:str=Query(..., description="skill name to search for (partial match allowed)"),
                         type:str=Query(..., description="Skill type (learn or teach)")
                         ):
    query = db.query(models.User).join(models.Skill)
    query=query.filter(models.Skill.name.ilike(f"{name}%"))

    if type:
        query=query.filter(models.Skill.type==type.lower())
    
    query = query.filter(models.User.email !=current_user["email"])
    users = query.all()
    return users
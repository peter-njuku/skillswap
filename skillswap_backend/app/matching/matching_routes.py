from fastapi import APIRouter, Depends, HTTPException
from ..database import db_dependancy
from . import matching_schemas
from .. import models
from typing import List
from ..auth.auth_utils import get_current_user

router=APIRouter(prefix="/match", tags=["Match"])

@router.get("/", response_model=List[matching_schemas.MatchResult])
def find_matches(db:db_dependancy, me:models.User = Depends(get_current_user)):
    if not me.skills_learn:
        raise HTTPException(status_code=400, detail="You must list skills you want to learn")
    my_learn_skills={s.strip().lower() for s in me.skills_learn.split(",") if s.strip()}

    candidates = db.query(models.User).filter(models.User.id !=me.id).all()

    matches = []

    for user in candidates:
        if not user.skills_teach:
            continue
        teach_skills = {s.strip().lower() for s in me.skills_teach.split(",") if s.strip()}

        if my_learn_skills & teach_skills:
            matches.append(user)

    return matches
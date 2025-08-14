from pydantic import BaseModel
from typing import List, Optional

class SkillBase(BaseModel):
    name:str
    type:str

class SkillCreate(SkillBase):
    pass

class SkillOut(SkillBase):
    id:int

    class Config:
        from_attributes = True

class UserProfileBase(BaseModel):
    email:str
    bio:Optional[str] = None

class UserProfileUpdate(UserProfileBase):
    skills:List[SkillCreate]

class UserProfileOut(BaseModel):
    id:int
    email:str
    skills:List[SkillOut]

    class Config:
        from_attributes=True
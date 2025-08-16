from pydantic import BaseModel
from typing import List, Optional

class MatchResult(BaseModel):
    user_id:int
    email:str
    full_name:Optional[str]
    skills_teach:List[str]
    skills_learn:List[str]

    class Config:
        from_attributes=True
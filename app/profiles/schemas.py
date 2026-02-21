from pydantic import BaseModel
from typing import Optional, List

class ProfileCreateUpdate(BaseModel):
    display_name: str
    creator_type: str
    organization_type: Optional[str] = None
    experience_level: Optional[str] = None
    platform:str
    audience_type:str
    goals: Optional[str] = None
    niches: List[str] = []

class ProfileResponse(BaseModel):
    model_config = {"from_attributes": True}  
    display_name: str
    creator_type: str
    organization_type: Optional[str]
    experience_level: Optional[str]
    platform:str
    audience_type:str
    goals: Optional[str]
    niches: List[str]
# src/schemas.py
from pydantic import BaseModel, Field, model_validator, ConfigDict, EmailStr
from enum import Enum
from datetime import datetime
from typing import List

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"

class SkillCategory(str, Enum):
    programming = "programming"
    music = "music"
    languages = "languages"
    science = "science"
    sport = "sport"

class SkillBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    category: SkillCategory
    level: SkillLevel
    
class SkillCreate(SkillBase):
    can_teach: bool
    want_learn: bool
    
    @model_validator(mode="after")
    def check_fields(self):
        if self.can_teach == self.want_learn:
            raise ValueError("You can't be teacher and student in single skill or neither.")
        return self
    
class SkillUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=500)
    category: SkillCategory | None = None
    level: SkillLevel | None = None
    can_teach: None = None
    want_learn: None = None
    
    @model_validator(mode="after")
    def check_teach_learn_fields(self):
        if self.can_teach is not None and self.want_learn is not None:
            if self.can_teach == self.want_learn:
                raise ValueError("You can't be teacher and student in a single skill or neither.")
        return self

class SkillResponse(SkillBase):
    id: int
    can_teach: bool
    want_learn: bool
    
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    email: EmailStr
    bio: str | None = Field(None, max_length=1000)
    is_active: bool | None = Field(True)

class UserCreate(UserBase):
    pass
    
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    skills: List[SkillResponse] = []
    
class UserUpdate(BaseModel):
    username: str | None = Field(None, max_length=100)
    email: EmailStr | None = None      
    bio: str | None = Field(None, max_length=1000)         
    is_active: bool | None = Field(None)

class ReviewCreate(BaseModel):
    exchange_id: int
    reviewed_id: int
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(None, max_length=1000)

class ReviewResponse(BaseModel):
    id: int
    exchange_id: int
    reviewer_id: int
    reviewed_id: int
    rating: int
    comment: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExchangeCreate(BaseModel):
    requester_id: int
    receiver_id: int
    skill_id: int
    message: str | None = Field(None, max_length=500)


class ExchangeUpdate(BaseModel):
    status: str 


class ExchangeResponse(BaseModel):
    id: int
    requester_id: int
    receiver_id: int
    skill_id: int
    status: str
    message: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


                
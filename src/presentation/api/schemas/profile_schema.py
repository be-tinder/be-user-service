from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from src.domain.enums import Gender

class UserRead(BaseModel):
    id: int
    name: Optional[str] = None
    phone_number: str
    gender: Gender = Gender.NOT_SPECIFIED
    sexual_orientation: Optional[str] = None
    birth_date: Optional[date] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    sexual_orientation: Optional[str] = None
    birth_date: Optional[date] = None

class UserDetail(UserRead):
    interests: List[str] = []
    photos: List[str] = []
    user_location: Optional[str] = None

from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.domain.enums import Gender
from src.presentation.api.schemas.user_image_schema import UserImageSchema


class UserListSchema(BaseModel):
    id: int
    images: List[UserImageSchema]
    name: str
    gender: Gender
    sexual_orientation: str
    birth_date: datetime


class UserRetrieveSchema(BaseModel):
    id: int
    images: List[UserImageSchema]
    name: str
    phone_number: str
    email: str
    gender: Gender
    sexual_orientation: str
    birth_date: datetime
    create_date: datetime
    update_date: datetime


class SignInSchema(BaseModel):
    phone_number: str


class OTPSchema(BaseModel):
    phone_number: str
    otp: str

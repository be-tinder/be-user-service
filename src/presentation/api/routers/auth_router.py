from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.application.auth.login_use_case import LoginUseCase
from src.domain.entities.user import UserDTO
from src.presentation.api.schemas.auth_schema import Token, LoginSchema

router = APIRouter()


@router.post("/login", response_model=Token)
@inject
async def login(form: LoginSchema, login_case: FromDishka[LoginUseCase]):
    return await login_case.execute(user=UserDTO(phone_number=form.phone_number))

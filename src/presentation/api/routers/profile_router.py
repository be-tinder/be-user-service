from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request

from src.application.auth.get_profile_use_case import GetProfileUseCase
from src.presentation.api.schemas.profile_schema import UserRead

router = APIRouter()


@router.get("/me", response_model=UserRead)
@inject
async def get_me(request: Request, profile_case: FromDishka[GetProfileUseCase]):
    return await profile_case(request.user.id)

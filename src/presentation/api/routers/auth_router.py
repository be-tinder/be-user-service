from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.application.users.user_retrieve_case import UserRetrieveUseCase
from src.presentation.api.schemas.user_schema import UserRetrieveSchema

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserRetrieveSchema)
@inject
async def get_user(
        user_id: int,
        user_retrieve_uc: FromDishka[UserRetrieveUseCase],
):
    user_data = await user_retrieve_uc.execute(user_id=user_id)
    return UserRetrieveSchema(**user_data)

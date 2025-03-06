from fastapi import APIRouter, Depends

from src.domain.entities.user import UserDTO
from src.domain.interfaces.use_case import IBaseUseCase
from src.presentation.api.depends.auth import get_current_user
from src.presentation.api.depends.get_use_case import get_use_case
from src.presentation.api.schemas.auth_schema import UserResponseSchema, AuthResponseSchema
from src.presentation.api.schemas.user_schema import SignInSchema

router = APIRouter()


@router.get("/me", response_model=UserResponseSchema)
async def get_me(me: UserDTO = Depends(get_current_user)) -> UserResponseSchema:
    return UserResponseSchema(status="success", details="User retrieved successfully", data=me)


@router.post("/send-sms", response_model=AuthResponseSchema)
async def sign_in(sign_in_form: SignInSchema, use_case: IBaseUseCase = Depends(get_use_case)) -> AuthResponseSchema:
    result = await use_case.execute(sign_in_form)
    return AuthResponseSchema(status="success", details="SMS sent successfully", data=result)


@router.post("/otp", response_model=AuthResponseSchema)
async def verify_otp(otp_form: dict, use_case: IBaseUseCase = Depends(get_use_case)) -> AuthResponseSchema:
    result = await use_case.execute(otp_form)
    return AuthResponseSchema(status="success", details="OTP verified successfully", data=result)

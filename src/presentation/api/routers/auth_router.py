from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.application.auth.login_use_case import LoginUseCase, LoginDTO
from src.application.auth.send_sms_use_case import RegisterDTO, SendSmsUseCase
from src.presentation.api.schemas.auth_schema import Token, LoginSchema, SendSmsSchema
from src.presentation.api.schemas.base_schema import BaseSchema

router = APIRouter()


@router.post("/verify-otp", response_model=Token)
@inject
async def verify_otp(form: LoginSchema, login_case: FromDishka[LoginUseCase]):
    return await login_case(LoginDTO(phone_number=form.phone_number, otp_code=form.otp_code))


@router.post("/send-otp", response_model=BaseSchema)
@inject
async def send_otp(form: SendSmsSchema, sms_case: FromDishka[SendSmsUseCase]):
    return await sms_case(RegisterDTO(phone_number=form.phone_number))

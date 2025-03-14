from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


class LoginSchema(BaseModel):
    phone_number: str
    otp_code: str


class SendSmsSchema(BaseModel):
    phone_number: str

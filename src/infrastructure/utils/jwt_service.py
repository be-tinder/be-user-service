import jwt

from src.domain.interfaces.jwt_service import IJWTService


class JWTService(IJWTService):
    def __init__(self, config):
        self.config = config

    def encode_jwt(self, user_id) -> str:
        payload = {
            "user_id": user_id,
        }
        return jwt.encode(payload=payload, key=self.config.JWT_ACCESS_TOKEN, algorithm="HS256")

    def decode_jwt(self, token):
        payload = jwt.decode(token, self.config.get.JWT_REFRESH_TOKEN, algorithms=["HS256"])
        return payload

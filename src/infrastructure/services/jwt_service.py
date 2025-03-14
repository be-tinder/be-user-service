import jwt

from src.domain.interfaces.security import IJWTService


class JWTService(IJWTService):
    def __init__(self, config):
        self.config = config

    def encode_jwt(self, user_id, is_refresh) -> str:
        payload = {
            "user_id": user_id,
        }
        key = self.config.JWT_ACCESS_TOKEN
        print(key)
        if is_refresh:
            key = self.config.JWT_ACCESS_TOKEN
        return jwt.encode(payload=payload, key=key, algorithm="HS256")

    def decode_jwt(self, token, is_refresh):
        key = self.config.JWT_REFRESH_TOKEN
        if is_refresh:
            key = self.config.JWT_REFRESH_TOKEN
        payload = jwt.decode(token, key, algorithms=["HS256"])
        return payload

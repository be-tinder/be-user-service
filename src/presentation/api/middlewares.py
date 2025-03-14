from typing import List

from dishka import Container
from fastapi import Request
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send

from src.domain.exceptions import AuthError
from src.domain.interfaces.security import IJWTService
from src.infrastructure.database.dao.user_dao import UserDao


class AuthMiddleware:
    def __init__(
            self,
            app: ASGIApp,
            container: Container,
            allowed_paths: List[str],
    ):
        self.app = app
        self.container = container
        self.allowed_paths = allowed_paths

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope)
        print(request.get("referer").split("/"))
        if request.headers.get("referer") in self.allowed_paths:
            await self.app(scope, receive, send)
            return
        user_dao = self.container.get(UserDao)
        jwt_service = self.container.get(IJWTService)

        auth_header = request.headers.get("authorization")
        if not auth_header:
            raise AuthError("No authorization header provided")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthError("Invalid authorization header format")

        token = parts[1]

        try:
            payload = jwt_service.decode_jwt(token, is_refresh=False)
        except Exception:
            raise AuthError("Invalid or expired token")

        user_id = payload.get("user_id")
        if not user_id:
            raise AuthError("User ID not found in token payload")

        db_user = await user_dao.get_user_by_id(user_id)
        if not db_user:
            raise AuthError("User not found or token invalid")

        scope["state"]["user"] = db_user

        await self.app(scope, receive, send)

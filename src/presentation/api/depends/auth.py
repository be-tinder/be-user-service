from dishka import FromDishka
from fastapi import Depends, HTTPException, status
from fastapi.security.http import HTTPBearer

from src.domain.entities.user import UserDTO
from src.domain.interfaces.security import IJWTService
from src.domain.repositories.iuser_repository import IUserRepository

token_auth = HTTPBearer()


async def get_current_user(
        jwt_service: FromDishka[IJWTService],
        user_repository: FromDishka[IUserRepository],
        token: str = Depends(token_auth)
) -> UserDTO:
    try:
        payload = jwt_service.decode_jwt(token)
        user_id = payload.get("user_id")
        db_user = await user_repository.get_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

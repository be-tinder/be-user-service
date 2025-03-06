from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

from src.container import AppContainer
from src.domain.entities.user import UserDTO
from src.domain.interfaces.jwt_service import IJWTService

token_auth = OAuth2PasswordBearer(tokenUrl="/api/token")


@inject
def get_current_user(
        jwt_service: IJWTService = Depends(Provide[AppContainer.jwt_service]),
        token: str = Depends(token_auth)
) -> UserDTO:
    try:
        payload = jwt_service.decode_jwt(token)
        return UserDTO(**payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

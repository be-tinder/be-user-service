from dishka import Provider, provide, Scope

from src.domain.interfaces.security import IJWTService
from src.infrastructure.config import Settings
from src.infrastructure.services.jwt_service import JWTService


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_jwt_service(self, settings: Settings) -> IJWTService:
        return JWTService(settings)
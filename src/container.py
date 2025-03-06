from dependency_injector import containers, providers

from src.domain.interfaces.use_case import IBaseUseCase
from src.infrastructure.config import get_settings
from src.infrastructure.database.alchemy_config import create_engine, create_session
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.utils.jwt_service import JWTService


class AppContainer(containers.DeclarativeContainer):
    """Dependency Injection Container for managing app-wide dependencies."""
    wiring_config = containers.WiringConfiguration(modules=["src.main"])

    config = providers.Configuration()
    settings = providers.Singleton(get_settings)

    engine = providers.Singleton(create_engine, db_url=config.DATABASE_URL)
    session_factory = providers.Singleton(create_session, engine=engine)

    jwt_service = providers.Factory(JWTService, config=settings)
    use_cases = providers.DependenciesContainer()

    user_repository = providers.Factory(
        UserRepository,
        session=providers.Factory(session_factory),
    )

    @classmethod
    def initialize_use_cases(cls):
        """Dynamically register all IBaseUseCase subclasses in the DI container."""
        for service_name, _cls in IBaseUseCase.subclasses.items():
            setattr(cls.use_cases, service_name, providers.Factory(_cls))

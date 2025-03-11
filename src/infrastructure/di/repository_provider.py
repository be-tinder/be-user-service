from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.iinterest_repository import IInterestRepository
from src.domain.repositories.iuser_bio_repository import IUserBioRepository
from src.domain.repositories.iuser_image_repository import IUserImageRepository
from src.domain.repositories.iuser_interested_repository import IUserInterestedRepository
from src.domain.repositories.iuser_location_repository import IUserLocationRepository
from src.domain.repositories.iuser_repository import IUserRepository
from src.infrastructure.database.repositories.interest_repository import InterestRepository
from src.infrastructure.database.repositories.user_bio_repository import UserBioRepository
from src.infrastructure.database.repositories.user_image_repository import UserImageRepository
from src.infrastructure.database.repositories.user_interested_repository import UserInterestedRepository
from src.infrastructure.database.repositories.user_location_repository import UserLocationRepository
from src.infrastructure.database.repositories.user_repository import UserRepository


class RepositoryIoc(Provider):
    """
    Central IOC container for all repositories.
    Each method yields an instance of a repository
    that uses the provided AsyncSession.
    """

    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession) -> AsyncIterable[IUserRepository]:
        """Provide an IUserRepository implementation with the given session."""
        yield UserRepository(session)

    @provide(scope=Scope.REQUEST)
    async def get_user_bio_repository(self, session: AsyncSession) -> AsyncIterable[IUserBioRepository]:
        """Provide an IUserBioRepository implementation with the given session."""
        yield UserBioRepository(session)

    @provide(scope=Scope.REQUEST)
    async def get_user_image_repository(self, session: AsyncSession) -> AsyncIterable[IUserImageRepository]:
        """Provide an IUserImageRepository implementation with the given session."""
        yield UserImageRepository(session)

    @provide(scope=Scope.REQUEST)
    async def get_interest_repository(self, session: AsyncSession) -> AsyncIterable[IInterestRepository]:
        """Provide an IInterestRepository implementation with the given session."""
        yield InterestRepository(session)

    @provide(scope=Scope.REQUEST)
    async def get_user_interested_repository(self, session: AsyncSession) -> AsyncIterable[IUserInterestedRepository]:
        """Provide an IUserInterestedRepository implementation with the given session."""
        yield UserInterestedRepository(session)

    @provide(scope=Scope.REQUEST)
    async def get_user_location_repository(self, session: AsyncSession) -> AsyncIterable[IUserLocationRepository]:
        """Provide an IUserLocationRepository implementation with the given session."""
        yield UserLocationRepository(session)

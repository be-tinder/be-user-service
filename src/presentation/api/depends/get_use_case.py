import inspect
from typing import Type

from src.container import AppContainer
from src.domain.interfaces.uow import IUoW
from src.domain.interfaces.repository import IRepository
from src.domain.interfaces.use_case import IBaseUseCase
from src.infrastructure.database.uow import UoW


def get_use_case(session):
    service_name = inspect.currentframe().f_code.co_name
    repository_name: Type[IRepository] = IRepository.get_sub_class()
    uow: Type[IUoW] = UoW(session)
    use_case = IBaseUseCase.get_sub_class(service_name)(repository_name, uow)
    use_case_provider = getattr(AppContainer.use_cases, service_name, None)

    if not use_case_provider:
        raise NotImplementedError(f"get_use_case() not implemented for {use_case_provider}")

    return use_case_provider()

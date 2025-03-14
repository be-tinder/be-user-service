from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.infrastructure.di_providers.dao_provider import DAOProvider
from src.infrastructure.di_providers.database_provider import DatabaseIoc
from src.infrastructure.di_providers.service_provider import ServiceProvider
from src.infrastructure.di_providers.use_case_provider import UseCaseProvider


def create_container():
    """Создаёт главный DI-контейнер"""
    container = make_async_container(
        DatabaseIoc(),
        DAOProvider(),
        ServiceProvider(),
        UseCaseProvider(),
        FastapiProvider(),
    )

    return container

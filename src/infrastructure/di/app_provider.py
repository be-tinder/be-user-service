from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.infrastructure.di.database_provider import DatabaseIoc
from src.infrastructure.di.repository_provider import RepositoryIoc
from src.infrastructure.di.service_provider import ServiceProvider
from src.infrastructure.di.use_case_provider import UseCaseProvider


def create_container():
    """Создаёт главный DI-контейнер"""
    container = make_async_container(
        DatabaseIoc(),
        RepositoryIoc(),
        UseCaseProvider(),
        ServiceProvider(),
        FastapiProvider(),
    )

    return container

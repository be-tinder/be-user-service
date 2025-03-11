from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.infrastructure.di.database_di import DatabaseIoc
from src.infrastructure.di.repository_di import RepositoryIoc
from src.infrastructure.di.use_case_di import UseCaseProvider


def create_container():
    """Создаёт главный DI-контейнер"""
    container = make_async_container(
        DatabaseIoc(),
        RepositoryIoc(),
        UseCaseProvider(),
        FastapiProvider())

    return container

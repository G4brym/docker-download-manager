from logging import Logger
from typing import get_type_hints

import injector

from downloads import Downloads
from downloads_infrastructure import DownloadsInfrastructure
from common.database import DatabaseHandler
from common.database_service import DatabaseService
from common.logger import provide_logger

__all__ = [
    "provider",
    "DatabaseService",
]


class Common(injector.Module):
    @injector.provider
    @injector.singleton
    def logger(self) -> Logger:
        return provide_logger()

    @injector.provider
    @injector.singleton
    def database(self) -> DatabaseService:
        return DatabaseHandler()


class ProvideManager(object):
    def __init__(self):
        self.injector = injector.Injector(
            [
                Common(),
                Downloads(),
                DownloadsInfrastructure(),
            ],
            auto_bind=True,
        )

    def inject(self, func):
        def wrapper(*args, **kwargs):
            for arg_name, arg_type in get_type_hints(func).items():
                try:
                    kwargs[arg_name] = self.injector.get(arg_type)
                except injector.CallError:
                    continue
            return func(*args, **kwargs)

        return wrapper


provider = ProvideManager()

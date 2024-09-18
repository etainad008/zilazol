from abc import ABC, abstractmethod
from api.constants import SERVER_TYPE
from constants import *
from requests import Response
from datetime import datetime


class FileServer(ABC):
    def __init__(self, type: SERVER_TYPE) -> None:
        self.type = type

    @staticmethod
    def check_response(res: Response):
        """Throws if the response is not OK. Should be called after every request."""
        if not res.ok:
            raise Exception(
                f"CODE {res.status_code}: {res.request.method} to {res.request.url} failed with body: {res.request.body}"
            )

    @abstractmethod
    def get_files(category: FILE_CATEGORY, amount: int) -> list:
        """Gets a certain amount of files of a specific type"""
        raise NotImplementedError()

    @abstractmethod
    def string_datetime_converter(value: str | datetime) -> str | datetime:
        """Converts the server's datetime representation to a string or the opposite."""
        raise NotImplementedError()


class FileServerCerberus(FileServer):
    def __init__(self) -> None:
        super().__init__(SERVER_TYPE.Cerberus)


class FileServerShufersal(FileServer):
    def __init__(self) -> None:
        super().__init__(SERVER_TYPE.Shufersal)


class FileServerSuperPharm(FileServer):
    def __init__(self) -> None:
        super().__init__(SERVER_TYPE.SuperPharm)

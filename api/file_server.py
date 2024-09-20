from abc import ABC, abstractmethod
from requests import Response
from datetime import datetime

from constants import *
from data_file import DataFile


class FileServer(ABC):
    def __new__(cls, type: SERVER_TYPE, creds: dict) -> "FileServer":
        match type:
            case SERVER_TYPE.Cerberus:
                return super().__new__(FileServerCerberus)
            case SERVER_TYPE.Shufersal:
                return super().__new__(FileServerShufersal)
            case SERVER_TYPE.SuperPharm:
                return super().__new__(FileServerSuperPharm)
            case SERVER_TYPE.Nibit:
                return super().__new__(FileServerNibit)
            case _:
                raise ValueError(f"Unsupported server type: {type}")

    def __init__(self, type: SERVER_TYPE, creds: dict) -> None:
        self.type = type
        self.creds = creds

    @staticmethod
    def check_response(res: Response):
        """Throws if the response is not OK. Should be called after every request."""
        if not res.ok:
            raise Exception(
                f"CODE {res.status_code}: {res.request.method} to {res.request.url} failed with body: {res.request.body}"
            )

    @abstractmethod
    def get_files(self, category: FILE_CATEGORY, amount: int) -> list[DataFile]:
        """Gets a certain amount of files of a specific type."""
        raise NotImplementedError()

    @abstractmethod
    def updated(self, category: FILE_CATEGORY) -> bool:
        """Returns wether there are new files in the given category."""
        raise NotImplementedError()

    @abstractmethod
    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        """Converts the server's datetime representation to a string or the opposite."""
        raise NotImplementedError()


class FileServerCerberus(FileServer):

    def get_files(self, category: FILE_CATEGORY, amount: int) -> list[DataFile]:
        pass

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass


class FileServerShufersal(FileServer):

    def get_files(self, category: FILE_CATEGORY, amount: int) -> list[DataFile]:
        pass

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass


class FileServerSuperPharm(FileServer):

    def get_files(self, category: FILE_CATEGORY, amount: int) -> list[DataFile]:
        pass

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass


class FileServerNibit(FileServer):

    def get_files(self, category: FILE_CATEGORY, amount: int) -> list[DataFile]:
        pass

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass

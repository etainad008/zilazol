from abc import ABC, abstractmethod
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import gzip

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

        self.base_url = SERVER_TYPE_DATA[self.type]["domain"]

    @staticmethod
    def check_response(res: requests.Response):
        """Throws if the response is not OK. Should be called after every request."""
        if not res.ok:
            raise Exception(
                f"CODE {res.status_code}: {res.request.method} to {res.request.url} failed with body: {res.request.body}"
            )

    @abstractmethod
    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
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

    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        pass

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass


class FileServerShufersal(FileServer):

    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        pass

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass


class FileServerSuperPharm(FileServer):

    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        pass

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass


class FileServerNibit(FileServer):
    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        content = self.update_parameters(
            chain,
            category,
            datetime.now(),
            additional_data.get("subchain", "") if additional_data is not None else "",
            additional_data.get("store_id", "") if additional_data is not None else "",
        )

        file_list = self.get_file_list(content, amount)

        return [
            DataFile(
                gzip.decompress(self.get_file_content(file["download_link"])),
                category=category,
                server_type=self.type,
            )
            for file in file_list
        ]

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass

    def get_file_content(self, download_url: str) -> bytes:
        res = requests.get(url=self.base_url + download_url)
        self.check_response(res)

        return res.content

    def get_file_list(self, content: bytes, amount: int) -> list:
        soup = BeautifulSoup(content, "lxml")
        rows = soup.select("#download_content table", limit=1)[0].find_all(
            "tr", limit=amount + 1  # +1 is for the table's header row
        )[1:]
        keys = [
            "name",
            "chain",
            "store",
            "category",
            "extension",
            "size",
            "timestamp",
            "download_link",
        ]

        file_list = []
        for row in rows:
            data = row.find_all("td")
            file_list.append(
                {
                    keys[i]: (
                        data[i].text.strip() if not data[i].a else data[i].a["href"]
                    )
                    for i in range(len(keys))
                }
            )

        return file_list

    def update_parameters(
        self,
        chain: CHAIN,
        category: FILE_CATEGORY,
        date: datetime = None,
        subchain: str = "",
        store_id: str = "",
    ) -> bytes:
        params = {
            "code": self.make_request_code(chain, subchain, store_id),
            "date": "" if date is None else date.strftime("%d/%m/%Y"),
            "fileType": SERVER_TYPE_DATA[self.type]["categories"][category][
                "parameter_name"
            ],
        }

        res = requests.get(url=SERVER_TYPE_DATA[self.type]["domain"], params=params)
        FileServer.check_response(res)

        return res.content

    def make_request_code(self, chain: CHAIN, subchain: str, store_id: str) -> str:
        chain_id = CHAINS_DATA[chain]["id"]
        return f"{chain_id}{subchain}{store_id}"

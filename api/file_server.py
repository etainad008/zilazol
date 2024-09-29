# TODO: Maybe we should not import everything in the global scope
#       requests is the biggest one but used all along the file :(
from abc import ABC, abstractmethod
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import etree
import json
import time

from constants import SERVER_TYPE, SERVER_TYPE_DATA, FILE_CATEGORY, CHAIN, CHAINS_DATA
from data_file import DataFile
from utils import unzip, ungzip


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
            case SERVER_TYPE.BinaProjects:
                return super().__new__(FileServerBinaProjects)
            case _:
                raise ValueError(f"Unsupported server type: {type}")

    def __init__(self, type: SERVER_TYPE, creds: dict) -> None:
        self.type = type
        self.creds = creds

        self.server_data = SERVER_TYPE_DATA[type]
        self.base_url = self.server_data["metadata"]["domain"]

    @staticmethod
    def check_response(res: requests.Response):
        """Throws if the response is not OK. Should be called after every request."""
        if not res.ok:
            raise Exception(
                f"CODE {res.status_code}: {res.request.method} to {res.request.url} failed with body: {res.request.body}"
            )

    def get_category_parameter_name(self, category: FILE_CATEGORY) -> str:
        return self.server_data["categories"][category]["parameter_name"]

    def is_chain_valid(self, chain: CHAIN) -> bool:
        valid_chains = [
            chain
            for chain in CHAIN
            if CHAINS_DATA[chain]["server"]["type"] == self.type
        ]
        if not chain in valid_chains:
            raise ValueError(
                f"Chain \"{chain.name}\" is not supported in \"{self.type.name}\" server; try using \"{CHAINS_DATA[chain]['server']['type'].name}\" server instead"
            )

    def get_subdomain_by_chain(self, chain: CHAIN) -> str:
        if not self.server_data["metadata"]["chain_by_subdomain"]:
            return self.base_url

        return self.server_data["metadata"]["domain"].format(
            CHAINS_DATA[chain]["server"]["domain_name"]
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
    LOGIN = "/login"
    USER = "/user"
    FILE_LIST = "/file/json/dir"
    FILE_DOWNLOAD = "/file/d"
    SUBMIT = "Sign in"

    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        self.is_chain_valid(chain)
        file_list, cftp = self.get_file_list(chain, category, amount)
        return [
            DataFile(
                self.get_file_content(
                    file["fname"], category == FILE_CATEGORY.Stores, cftp
                ),
                chain,
                category,
            )
            for file in file_list
        ]

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass

    def get_file_content(self, file_name: str, is_xml: bool, cftp: str) -> bytes:
        download_url = f"{self.base_url}{self.FILE_DOWNLOAD}/{file_name}"
        res = requests.get(url=download_url, cookies={"cftpSID": cftp})
        FileServer.check_response(res)

        if is_xml:
            return res.content

        return ungzip(res.content)

    def extract_csrf(self, content: bytes):
        soup = BeautifulSoup(content, "lxml")
        csrf_token = soup.find("meta", attrs={"name": "csrftoken"})["content"]

        return csrf_token

    def login(self, chain: CHAIN):
        login_url = self.base_url + self.LOGIN
        user_url = self.base_url + self.LOGIN + self.USER

        res = requests.get(url=login_url)
        FileServer.check_response(res)

        csrf_token = self.extract_csrf(res.content)
        cftp_token = res.cookies.get("cftpSID")

        username = CHAINS_DATA[chain]["server"]["creds"]["username"]
        password = CHAINS_DATA[chain]["server"]["creds"]["password"]
        login_params = {
            "r": "",
            "username": username,
            "password": password,
            "Submit": self.SUBMIT,
            "csrftoken": csrf_token,
        }
        headers = {"Cookie": f"cftpSID={cftp_token}"}

        # /login/user redirects to /file
        res = requests.post(url=user_url, params=login_params, headers=headers)
        FileServer.check_response(res)

        return (self.extract_csrf(res.content), res.cookies.get("cftpSID"))

    def get_file_list(
        self,
        chain: CHAIN,
        category: FILE_CATEGORY,
        amount: int,
        date: datetime = datetime.today(),
        store_id: str = None,
    ) -> list:
        csrf, cftp = self.login(chain)
        body_params = {
            "iDisplayLength": amount,  # how many we want the server to return
            "mDataProp_1": "typeLabel",
            "sSearch_1": "file",  # we only want files
            "sSearch": self.get_search_string(chain, category, store_id, date),
            "csrftoken": csrf,
        }
        headers = {"Cookie": f"cftpSID={cftp}"}

        res = requests.post(
            url=self.base_url + self.FILE_LIST, headers=headers, data=body_params
        )
        FileServer.check_response(res)

        data = res.json()
        file_list = list(data.get("aaData"))

        return file_list, cftp

    def get_search_string(
        self,
        chain: CHAIN,
        category: FILE_CATEGORY,
        store_id: str = None,
        date: datetime = None,
    ) -> str:
        string = f"{self.get_category_parameter_name(category=category)}{CHAINS_DATA[chain]['id']}"

        if not store_id is None and category != FILE_CATEGORY.Stores:
            string += f"-{store_id}"

        if not date is None:
            string += f"-{date.strftime('%Y%m%d')}"

        return string

    def time_string_to_datetime(time: str):
        return datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")


class FileServerShufersal(FileServer):
    SHUFERSAL_UPDATE_CATEGORY = "/FileObject/UpdateCategory"

    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        self.is_chain_valid(chain)
        self.get_affinity_tokens()
        res = self.update_categories(category=category)
        self.check_response(res)
        file_list = self.get_file_list(res.content)

        return [
            DataFile(
                chain, self.get_file_content(file["download_link"]), category=category
            )
            for file in file_list[:amount]
        ]

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass

    def get_affinity_tokens(self):
        res = requests.get(url=self.base_url)
        self.check_response(res)

        ARRaffinity = res.cookies.get_dict().get("ARRAffinity")
        ARRAffinitySameSite = res.cookies.get_dict().get("ARRAffinitySameSite")

        return (ARRaffinity, ARRAffinitySameSite)

    def update_categories(
        self,
        category=FILE_CATEGORY,
        store=0,  # All
    ):
        params = {"catID": self.get_category_parameter_name(category), "storeId": store}
        res = requests.get(self.base_url + self.SHUFERSAL_UPDATE_CATEGORY, data=params)
        self.check_response(res)

        return res

    def get_file_list(self, content: bytes):
        soup = BeautifulSoup(content, "lxml")
        rows = soup.select("tr.webgrid-row-style, tr.webgrid-alternating-row")
        keys = [
            "download_link",
            "timestamp",
            "size",
            "format",
            "category",
            "address",
            "name",
            "sort_id",
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

    def get_file_content(self, url_download: str) -> bytes:
        res = requests.get(url=url_download)
        self.check_response(res)

        return ungzip(res.content)

    def get_prices(self, amount: int) -> list:
        self.get_affinity_tokens()
        res = self.update_categories()
        self.check_response(res)
        file_list = self.get_file_list(res.content)

        return [
            self.get_file_content(file["download_link"]) for file in file_list[:amount]
        ]


class FileServerSuperPharm(FileServer):
    SUPER_PHARM_SESSION_COOKIE = "ci_session"

    def hebrew_ascii_to_utf8(self, hebrew_bytes: bytes):
        decoded_bytes = hebrew_bytes.decode("ISO-8859-8", errors="ignore")
        parser = etree.XMLParser(encoding="utf-8")
        root = etree.fromstring(decoded_bytes.encode("utf-8"), parser)
        utf8_bytes = etree.tostring(root, pretty_print=True, encoding="utf-8")

        return utf8_bytes

    def time_to_date_string(time: datetime = None):
        if time is None:
            time = datetime.today()

        return time.strftime("%Y-%m-%d")

    def update_categories(
        self,
        category: FILE_CATEGORY,
        date=time_to_date_string(),
        store="",
    ):
        params = {
            "type": self.get_category_parameter_name(category),
            "date": date,
            "store": "",  # for the meantime, this is "All"
        }
        res = requests.get(self.base_url, params=params)
        self.check_response(res)

        return (res, res.cookies.get_dict().get(self.SUPER_PHARM_SESSION_COOKIE))

    def get_file_list(self, content: bytes):
        soup = BeautifulSoup(content, "lxml")
        rows = soup.select(
            ".file_list table tr:nth-child(n+2)"
        )  # each page has only 20 rows so there are no performance issues like in Nibit
        keys = [
            "sort_id",
            "name",
            "timestamp",
            "category",
            "branch_name",
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

    def get_file_content(self, download_url: str, cookie: str) -> bytes:
        auth_cookie = {self.SUPER_PHARM_SESSION_COOKIE: cookie}
        download_res = requests.get(
            url=self.base_url + download_url, cookies=auth_cookie
        )
        self.check_response(download_res)
        download_descriptor = download_res.json()
        res = requests.get(
            url=self.base_url + download_descriptor["href"], cookies=auth_cookie
        )
        self.check_response(res)

        return self.hebrew_ascii_to_utf8(unzip(res.content))

    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        self.is_chain_valid(chain)
        res, cookie = self.update_categories(category=category)
        file_list = self.get_file_list(res.content)

        return [
            DataFile(
                chain,
                self.get_file_content(file["download_link"], cookie),
                category=category,
            )
            for file in file_list[:amount]
        ]

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass


class FileServerNibit(FileServer):
    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        self.is_chain_valid(chain)
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
                chain,
                ungzip(self.get_file_content(file["download_link"])),
                category=category,
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
        )[
            1:
        ]  # this method is faster than selecting tr:nth-child(n+2)
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
            "fileType": self.get_category_parameter_name(category),
        }

        res = requests.get(url=self.base_url, params=params)
        FileServer.check_response(res)

        return res.content

    def make_request_code(self, chain: CHAIN, subchain: str, store_id: str) -> str:
        chain_id = CHAINS_DATA[chain]["id"]
        return f"{chain_id}{subchain}{store_id}"


class FileServerBinaProjects(FileServer):

    def get_files(
        self, chain: CHAIN, category: FILE_CATEGORY, amount: int, additional_data=None
    ) -> list[DataFile]:
        self.is_chain_valid(chain)
        file_list = self.update_parameters(
            chain=chain, category=category, date=datetime.today()
        )

        return [
            DataFile(
                chain,
                unzip(self.get_file_content(chain, file["FileNm"])),
                category=category,
            )
            for file in file_list
        ]

    def updated(self, category: FILE_CATEGORY) -> bool:
        pass

    def string_datetime_converter(self, value: str | datetime) -> str | datetime:
        pass

    def get_file_content(self, chain: CHAIN, filename: str) -> bytes:
        params = {"FileNm": filename}
        download_url = requests.get(
            url=self.get_subdomain_by_chain(chain) + "/Download.aspx", params=params
        )
        FileServer.check_response(download_url)

        res = requests.get(url=json.loads(download_url.text)[0]["SPath"])
        FileServer.check_response(res)

        return res.content

    def get_file_list(self, content: str, amount: int) -> list:
        return json.loads(content)[:amount]

    def update_parameters(
        self,
        chain: CHAIN,
        category: FILE_CATEGORY,
        date: datetime = None,
        store_id: str = "0",  # all
    ) -> list:
        params = {
            "_": int(time.time()),
            "WStore": store_id,
            "WFileType": self.get_category_parameter_name(category),
            "WDate": "" if date is None else date.strftime("%d/%m/%Y"),
        }
        res = requests.get(
            url=self.get_subdomain_by_chain(chain) + "/MainIO_Hok.aspx", params=params
        )
        FileServer.check_response(res)

        return res.json()

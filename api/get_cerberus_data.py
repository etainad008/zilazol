import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gzip


CERBERUS_BASE_URL = "https://url.publishedprices.co.il"
CERBERUS_LOGIN = "/login"
CERBERUS_USER = "/user"
CERBERUS_FILE_METADATA = "/file/json/dir"
CERBERUS_FILE_DOWNLOAD = "/file/d"
CERBERUS_SUBMIT = "Sign in"
CERBERUS_CHAINS = {
    "doralon": {
        "password": "",
        "chain_id": "7290492000005"
    },
    "TivTaam": {
        "password": "",
        "chain_id": "7290873255550"
    },
    "HaziHinam": {
        "password": "",
        "chain_id": "7290700100008"
    },
    "yohananof": {
        "password": "",
        "chain_id": "7290100700006"
    },
    "osherad": {
        "password": "",
        "chain_id": "7290103152017"
    },
    "SalachD": {
        "password": "12345",
        "chain_id": "7290526500006"
    },
    "Stop_Market": {
        "password": "",
        "chain_id": "7290639000004"
    },
    "politzer": {
        "password": "",
        "chain_id": "7291059100008"
    },
    "Paz_bo": {
        "password": "paz468",
        "chain_id": "7290644700005"
    },
    "freshmarket": {
        "password": "",
        "chain_id": "7290876100000"
    },
    "Keshet": {
        "password": "",
        "chain_id": "7290785400000"
    },
    "RamiLevi": {
        "password": "",
        "chain_id": "7290058140886"
    },
    "SuperCofixApp": {
        "password": "",
        "chain_id": "7291056200008"
    }
}


def get_chain_prices(chain: str, amount: int) -> list:
    file_list, cftp = get_file_list(chain, amount, "PriceFull")
    return [get_file_content(file["fname"], cftp) for file in file_list]


def get_file_content(file_name: str, cftp: str) -> bytes:
    url_download = f"{CERBERUS_BASE_URL}{CERBERUS_FILE_DOWNLOAD}/{file_name}"
    res = requests.get(url=url_download, cookies={"cftpSID": cftp})
    check_response(res)

    return gzip.decompress(res.content)
    

def get_tokens(url: str):
    res = requests.get(url)
    check_response(res)

    return extract_tokens(res)


def post_tokens(url: str, headers: dict = {}, params: dict = {}):
    res = requests.post(url, headers=headers, data=params)
    check_response(res)

    return extract_tokens(res)


def check_response(res: requests.Response):
    if not res.ok:
        raise Exception(f"CODE {res.status_code}: {res.request.method} to {res.request.url} failed with body: {res.request.body}")


def extract_tokens(res: requests.Response):
    cftp = res.cookies.get("cftpSID")
    csrf = extract_csrf(res.content)

    return (cftp, csrf)


def extract_csrf(content: bytes):
    soup = BeautifulSoup(content, "lxml")
    csrf_token = soup.find("meta", attrs={"name": "csrftoken"})["content"]

    return csrf_token
    

def login(chain: str) -> tuple:
    """Logs in into the Cerberus FTP server
    with the specified chain and password,
    and returns the file tokens."""
    login_url = CERBERUS_BASE_URL + CERBERUS_LOGIN
    user_url = CERBERUS_BASE_URL + CERBERUS_LOGIN + CERBERUS_USER

    cftp, csrf = get_tokens(login_url)
    headers = {"Cookie": f"cftpSID={cftp}"}
    password = CERBERUS_CHAINS[chain]["password"]
    login_params = {"r": "", "username": chain, "password": password, "Submit": CERBERUS_SUBMIT, "csrftoken": csrf}

    # /login/user redirects to /file
    return post_tokens(user_url, headers=headers, params=login_params)


def get_file_list(chain: str, amount: int = 100, search: str = ""):
    """Returns the file list from the server along with the cftp token for downloading."""
    if amount < 1:
        raise Exception("Amount must be positive")

    cftp, csrf = login(chain)
    cookies = {"cftpSID": cftp}
    body_params = {
        'iDisplayLength': amount, # how many we want the server to return
        'mDataProp_1': 'typeLabel',
        'sSearch_1': 'file', # we only want files
        'sSearch': search,
        'csrftoken': csrf
    }

    res = requests.post(url=CERBERUS_BASE_URL + CERBERUS_FILE_METADATA, cookies=cookies, data=body_params)
    check_response(res)

    data = res.json()
    file_list = list(data.get("aaData"))
    file_list.sort(key=lambda file: time_string_to_datetime(file["time"]), reverse=True) # we want the newest first
    
    return (file_list, cftp)


def time_string_to_datetime(time: str):
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gzip
from enum import Enum


SHUFERSAL_BASE_URL = "https://prices.shufersal.co.il"
SHUFERSAL_UPDATE_CATEGORY = "/FileObject/UpdateCategory"
SHUFERSAL_CATEGORIES = Enum("SHUFERSAL_CATEGORIES", {name: i for i, name in enumerate(['All', 'Prices', 'PricesFull', 'Promos', 'PromosFull', 'Stores'])})
SHUFERSAL_STORES = Enum("SHUFERSAL_STORES", { "All": 0 })


def get_affinity_tokens():
    res = requests.get(url=SHUFERSAL_BASE_URL)
    check_response(res)
    
    ARRaffinity = res.cookies.get_dict().get("ARRAffinity")
    ARRAffinitySameSite = res.cookies.get_dict().get("ARRAffinitySameSite")

    return (ARRaffinity, ARRAffinitySameSite)
    

def update_categories(category = SHUFERSAL_CATEGORIES.PricesFull.value, store = SHUFERSAL_STORES.All.value):
    params = {
        "catID": category,
        "storeId": store
    }
    res = requests.get(SHUFERSAL_BASE_URL + SHUFERSAL_UPDATE_CATEGORY, data=params)
    check_response(res)

    return res


def get_file_list(content: bytes):
    soup = BeautifulSoup(content, "lxml")
    rows = soup.select('tr.webgrid-row-style, tr.webgrid-alternating-row')
    keys = ['download_link', 'timestamp', 'size', 'format', 'category', 'address', 'name', 'sort_id']
    
    file_list = []
    for row in rows:
        data = row.find_all("td")
        file_list.append(
            { keys[i]: data[i].text.strip() if not data[i].a else data[i].a['href'] for i in range(len(keys)) }
        )

    file_list = [file for file in file_list if "KB" in file["size"]]
    file_list.sort(key=lambda file: float(file['size'].split(" ")[0]), reverse=True)

    return file_list


def get_file_content(url_download: str) -> bytes:
    res = requests.get(url=url_download)
    check_response(res)

    return gzip.decompress(res.content)


def get_prices(amount: int) -> list:
    get_affinity_tokens()
    res = update_categories()
    file_list = get_file_list(res.content)
    return [get_file_content(file["download_link"]) for file in file_list][:amount]
    

def check_response(res: requests.Response):
    if not res.ok:
        raise Exception(f"CODE {res.status_code}: {res.request.method} to {res.request.url} failed with body: {res.request.body}")

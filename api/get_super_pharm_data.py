import requests
from bs4 import BeautifulSoup
from datetime import datetime
from enum import Enum
import json
import zipfile
import io
from lxml import etree


SUPER_PHARM_BASE_URL = 'https://prices.super-pharm.co.il'
SUPER_PHARM_CATEGORIES = Enum('SUPER_PHARM_CATEGORIES', { 'All': '', 'Prices': 'Price', 'PricesFull': 'PriceFull', 'Promos': 'Promo', 'PromosFull': 'PromoFull', 'Stores': 'StoresAll'})
SUPER_PHARM_STORES = Enum('SHUFERSAL_STORES', { 'All': '' })
SUPER_PHARM_SESSION_COOKIE = "ci_session"


def hebrew_ascii_to_utf8(hebrew_bytes: bytes):

    decoded_bytes = hebrew_bytes.decode('ISO-8859-8', errors="ignore")
    parser = etree.XMLParser(encoding='utf-8')
    root = etree.fromstring(decoded_bytes.encode('utf-8'), parser)
    utf8_bytes = etree.tostring(root, pretty_print=True, encoding='utf-8')

    return utf8_bytes


def time_to_date_string(time: datetime = None):
    if time is None:
        time = datetime.today()
        
    return time.strftime('%Y-%m-%d')


def unzip(zip_bytes: bytes) -> bytes:
    stream = io.BytesIO(zip_bytes)

    with zipfile.ZipFile(stream, 'r') as zip:
        file_name = zip.namelist()[0]  # We only have one file every time
        
        with zip.open(file_name) as f:
            file_bytes = f.read()
    
    return file_bytes


def update_categories(category = SUPER_PHARM_CATEGORIES.PricesFull.value, date = time_to_date_string(), store = SUPER_PHARM_STORES.All.value):
    params = {
        'type': category,
        'date': date,
        'store': store
    }
    res = requests.get(SUPER_PHARM_BASE_URL, params=params)
    check_response(res)

    return (res, res.cookies.get_dict().get(SUPER_PHARM_SESSION_COOKIE))


def get_file_list(content: bytes):
    soup = BeautifulSoup(content, 'lxml')
    rows = soup.select('.file_list table tr:nth-child(n+2)')
    keys = ['sort_id', 'name', 'timestamp', 'category', 'branch_name', 'download_link']
    
    file_list = []
    for row in rows:
        data = row.find_all('td')
        file_list.append(
            { keys[i]: data[i].text.strip() if not data[i].a else data[i].a['href'] for i in range(len(keys)) }
        )

    return file_list


def get_file_content(url_download: str, cookie: str) -> bytes:
    auth_cookie = { SUPER_PHARM_SESSION_COOKIE: cookie }
    download_res = requests.get(url=SUPER_PHARM_BASE_URL + url_download, cookies=auth_cookie)
    download_descriptor = json.loads(download_res.content.decode('utf-8'))
    res = requests.get(url=SUPER_PHARM_BASE_URL + download_descriptor["href"], cookies=auth_cookie)
    check_response(res)

    return hebrew_ascii_to_utf8(unzip(res.content))


def get_prices(amount: int) -> list:
    res, cookie = update_categories()
    file_list = get_file_list(res.content)
    return [get_file_content(file['download_link'], cookie) for file in file_list[:amount]]
    

def check_response(res: requests.Response):
    if not res.ok:
        raise Exception(f'CODE {res.status_code}: {res.request.method} to {res.request.url} failed with body: {res.request.body}')

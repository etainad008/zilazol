import re
import xmltodict


BASE_UNITS = ['גר', 'ליטר', 'מל', 'מ"ל', 'ג', 'קג', 'יח', 'יח\'', 'גרם', 'מיליליטר']
UNITS = [bytes(unit, encoding="utf-8") for unit in BASE_UNITS]


def process(blob: bytes) -> str:
    # not perfect, but good enough for the meantime.
    # maybe / unit \d+ / ??
    quantity_re = re.compile(br"\s+\d+\s+")
    unit_list = [(br"\s+" + unit + br"\s+") for unit in UNITS]
    unit_list.extend([unit + b"$" for unit in UNITS])
    unit_re = re.compile(br"|".join(unit_list))
    return (unit_re.sub(repl=b" ", string=quantity_re.sub(repl=b" ", string=blob))).decode(encoding="utf-8").strip()


def to_json(blob: bytes):
    return xmltodict.parse(blob, encoding="utf-8")

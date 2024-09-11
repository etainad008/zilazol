import re
import xmltodict


UNITS = ['גר', 'ליטר', 'מל', 'מ"ל', 'ג', 'קג', 'יח', 'יח\'']


def process(blob: bytes) -> bytes:
    # not perfect, but good enough for the meantime
    quantity_re = re.compile(br"\s+\d+\s+")
    unit_re = re.compile(br"|".join([(br"\s+" + bytes(unit, encoding="utf-8") + br"\s+") for unit in UNITS]))
    return unit_re.sub(repl=b" ", string=quantity_re.sub(repl=b" ", string=blob))


def to_json(blob: bytes):
    return xmltodict.parse(blob, encoding="utf-8")


if __name__ == "__main__":
    pass
    # data = get_chain_prices("RamiLevi", 1)[0][:20000]
    # with open("idkkk.xml", "wb") as f:
    #     f.write(process(data))

    # with open("idkkk2.xml", "wb") as f:
    #     f.write(data)

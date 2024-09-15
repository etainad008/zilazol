from collections import defaultdict
from api.process_data import process


def get_unique_names(chain_prices: list, common: int):
    cache = defaultdict(set)

    for prices in chain_prices:
        try:
            for item in prices.get("root", prices.get("Root"))["Items"]["Item"]:
                try:
                    item["ItemName"] = process(bytes(item["ItemName"], encoding="utf-8"))
                    cache[(item['ItemName'], item['ItemCode'])].add(prices.get("root", prices.get("Root"))["ChainId"])
                except:
                    pass
        except:
            with open("woww.json", "wb") as f:
                f.write(bytes(str(prices), encoding="utf-8"))

    return { k: v for k, v in cache.items() if len(v) >= common }
# i love my dad

if __name__ == "__main__":
    from get_cerberus_data import get_chain_prices, CERBERUS_CHAINS
    from api.process_data import to_json
    from db import get_unique_names

    a = []
    for chain_name in CERBERUS_CHAINS.keys():
        for prices in get_chain_prices(chain_name, 10):
            a.append(to_json(prices))

    for i in range(2, 7):
        names = get_unique_names(a, i)

        print(f"{i}: number of products is {len(names)}")
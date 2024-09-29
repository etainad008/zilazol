import xmltodict

from entity import Entity
from constants import *
from data_file import DataFile

SHUFERSAL_SUBCHAIN_NAME_FALLBACK = {
    "1": "שופרסל שלי",
    "50": "יש בשכונה",
    "7": "שופרסל אקספרס",
    "2": "שופרסל דיל",
    "5": "Be",
    "6": "יש חסד",
    "4": "שופרסל דיל אקסטרא",
    "18": "גוד מרקט",
    "3": "שערי רווחה",
}


class Parser:
    def __init__(self) -> None:
        pass

    def parse(self, file: DataFile) -> list[Entity]:
        data = xmltodict.parse(file.content)
        server_type = CHAINS_DATA[file.chain]["server"]["type"]
        chain_id = CHAINS_DATA[file.chain]["id"]

        if server_type == SERVER_TYPE.Shufersal:
            subchain_cache = set()
            subchain_dict = {}
            stores = []
            subchains = []
            store_list = data["asx:abap"]["asx:values"]["STORES"]["STORE"]
            if isinstance(store_list, dict):
                store_list = [store_list]

            for store in store_list:
                subchain_id = str(int(store["SUBCHAINID"]))
                if not subchain_id in subchain_cache:
                    subchain_cache.add(subchain_id)
                    subchains.append(
                        Entity(
                            {
                                self.create_subchain(
                                    subchain_id,
                                    chain_id,
                                    store["SUBCHAINNAME"]
                                    or SHUFERSAL_SUBCHAIN_NAME_FALLBACK[subchain_id],
                                )
                            }
                        )
                    )

                stores.append(
                    Entity(
                        self.create_store(
                            store["STOREID"],
                            chain_id,
                            store["SUBCHAINID"],
                            store["BIKORETNO"],
                            store["STORETYPE"],
                            store["STORENAME"],
                            store["ADDRESS"],
                            store["CITY"],
                            store["ZIPCODE"],
                        )
                    )
                )

            return (subchains, stores)

        elif server_type == SERVER_TYPE.Cerberus:
            subchain_list = data["Root"]["SubChains"]["SubChain"]
            if isinstance(subchain_list, dict):
                subchain_list = [subchain_list]

            subchains = []
            stores = []

            for subchain in subchain_list:
                subchains.append(
                    Entity(
                        self.create_subchain(
                            subchain["SubChainId"], chain_id, subchain["SubChainName"]
                        )
                    )
                )
                store_list = subchain["Stores"]["Store"]
                if isinstance(store_list, dict):
                    store_list = [store_list]

                stores.extend(
                    [
                        Entity(
                            self.create_store(
                                store["StoreId"],
                                chain_id,
                                subchain["SubChainId"],
                                store["BikoretNo"],
                                store["StoreType"],
                                store["StoreName"],
                                store["Address"],
                                store["City"],
                                store["ZipCode"],
                            )
                        )
                        for store in store_lists
                    ]
                )

            return (subchains, stores)

        elif server_type == SERVER_TYPE.Nibit:
            subchain_cache = set()
            stores = []
            subchains = []
            store_list = data["Store"]["Branches"]["Branch"]
            if isinstance(store_list, dict):
                store_list = [store_list]

            for store in store_list:
                subchain_id = str(int(store["SubChainID"]))
                if not subchain_id in subchain_cache:
                    subchain_cache.add(subchain_id)
                    subchains.append(
                        Entity(
                            self.create_subchain(
                                subchain_id,
                                chain_id,
                                store["SubChainName"],
                            )
                        )
                    )

                stores.append(
                    Entity(
                        self.create_store(
                            store["StoreID"],
                            chain_id,
                            store["SubChainID"],
                            store["BikoretNo"],
                            store["StoreType"],
                            store["StoreName"],
                            store["Address"],
                            store["City"],
                            store["ZIPCode"],
                        )
                    )
                )

            return (subchains, stores)

        elif server_type == SERVER_TYPE.BinaProjects:
            subchain_list = data["Root"]["SubChains"]["SubChain"]
            if isinstance(subchain_list, dict):
                subchain_list = [subchain_list]

            subchains = []
            stores = []

            for subchain in subchain_list:
                subchains.append(
                    Entity(
                        self.create_subchain(
                            subchain["SubChainId"],
                            chain_id,
                            subchain["SubChainName"],
                        )
                    )
                )
                store_list = subchain["Stores"]["Store"]
                if isinstance(store_list, dict):
                    store_list = [store_list]

                stores.extend(
                    [
                        Entity(
                            self.create_store(
                                store["StoreId"],
                                chain_id,
                                subchain["SubChainId"],
                                store["BikoretNo"],
                                store["StoreType"],
                                store["StoreName"],
                                store["Address"],
                                store["City"],
                                store["ZipCode"],
                            )
                        )
                        for store in store_list
                    ]
                )

            return (subchains, stores)

        elif server_type == SERVER_TYPE.SuperPharm:
            root = data["OrderXml"]["Envelope"]
            store_list = root["Header"]["Details"]["Line"]
            if isinstance(store_list, dict):
                store_list = [store_list]

            chain_id = root["ChainId"]
            subchain_id = root["SubChainId"]

            stores = [
                Entity(
                    self.create_store(
                        store["StoreId"],
                        chain_id,
                        subchain_id,
                        store["BikoretNo"],
                        store["StoreType"],
                        store["StoreName"],
                        store["Address"],
                        store["City"],
                        store["ZipCode"],
                    )
                )
                for store in store_list
            ]

            return (
                [
                    Entity(
                        self.create_subchain(
                            subchain_id, chain_id, store_list[0]["SubChainName"]
                        ),
                    )
                ],
                stores,
            )

    def create_store(
        self,
        id: str,
        chain_id: str,
        subchain_id: str,
        bikoret_number: str,
        type: str,
        name: str,
        address: str,
        city: str,
        zip_code: str,
    ) -> dict:
        return {
            "id": self.normalize_number(id),
            "chain_id": chain_id,
            "subchain_id": self.normalize_number(subchain_id),
            "bikoret_number": self.normalize_number(bikoret_number),
            "type": type,
            "name": name,
            "address": address,
            "city": city,
            "zip_code": self.normalize_number(zip_code),
        }

    def create_subchain(self, id: str, chain_id: str, name: str) -> dict:
        return {
            "id": self.normalize_number(id),
            "chain_id": chain_id,
            "name": name,
        }

    def normalize_number(self, number: str) -> str:
        return str(int(number))


if __name__ == "__main__":
    with open(
        r"C:\Users\etain\Downloads\StoresFull7290172900007--202409290200.xml",
        "rb",
    ) as f:
        file = DataFile(f.read(), CHAIN.SuperPharm, FILE_CATEGORY.Stores)

    import timeit

    # with open(
    #     r"/Users/shellyvelan/Desktop/Babi R's Folder/zilazol/api/TivTaam_Stores.xml",
    #     "rb",
    # ) as f:
    #     file2 = DataFile(f.read(), CHAIN.TivTaam, FILE_CATEGORY.Stores)
    # from file_server import FileServer

    # chain = CHAIN.RamiLevi
    # server = FileServer(SERVER_TYPE.Cerberus, CHAINS_DATA[chain]["server"]["creds"])

    # file2 = server.get_files(chain, FILE_CATEGORY.Stores, 1)[0]

    # parser = Parser()
    # # parser.parse(file)
    # a = parser.parse(file)
    # pass

    # print(
    #     timeit.timeit(lambda: str(int("00100")), number=4000000),
    #     timeit.timeit(lambda: "00100".lstrip("0"), number=4000000),
    # )

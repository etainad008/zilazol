from abc import ABC, abstractmethod
import xmltodict

from entity import Entity
from constants import *
from data_file import DataFile
from file_server import FileServer
from database import Database

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

STORE_TYPE = {
    "1": "physical",
    "2": "online",
    "3": "physical_and_online",
    None: "physical",
    "": "physical",
}


class BaseParser(ABC):
    """Defines an interface for a parser which every server type needs to implement."""

    @abstractmethod
    def parse_items_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        """Returns the item list parsed from the given file."""
        pass

    @abstractmethod
    def parse_promos_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        """Returns the promo list parsed from the given file."""
        pass

    @abstractmethod
    def parse_stores_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> tuple[list[Entity], list[Entity]]:
        """Returns the subchain list and store list parsed from the given file."""
        pass


class ParserCerberus(BaseParser):

    def parse_items_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_promos_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_stores_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> tuple[list[Entity], list[Entity]]:
        subchain_list = data["Root"]["SubChains"]["SubChain"]
        if isinstance(subchain_list, dict):
            subchain_list = [subchain_list]

        subchains = []
        stores = []

        for subchain in subchain_list:
            subchains.append(
                Entity(
                    ParserUtils.create_subchain(
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
                        ParserUtils.create_store(
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


class ParserShufersal(BaseParser):

    def parse_items_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_promos_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_stores_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> tuple[list[Entity], list[Entity]]:
        subchain_cache = set()
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
                        ParserUtils.create_subchain(
                            subchain_id,
                            chain_id,
                            store["SUBCHAINNAME"]
                            or SHUFERSAL_SUBCHAIN_NAME_FALLBACK[subchain_id],
                        )
                    )
                )

            stores.append(
                Entity(
                    ParserUtils.create_store(
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


class ParserSuperPharm(BaseParser):

    def parse_items_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_promos_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_stores_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> tuple[list[Entity], list[Entity]]:
        root = data["OrderXml"]["Envelope"]
        store_list = root["Header"]["Details"]["Line"]
        if isinstance(store_list, dict):
            store_list = [store_list]

        chain_id = root["ChainId"]
        subchain_id = root["SubChainId"]

        stores = [
            Entity(
                ParserUtils.create_store(
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
                    ParserUtils.create_subchain(
                        subchain_id, chain_id, store_list[0]["SubChainName"]
                    ),
                )
            ],
            stores,
        )


class ParserNibit(BaseParser):

    def parse_items_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_promos_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_stores_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> tuple[list[Entity], list[Entity]]:
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
                        ParserUtils.create_subchain(
                            subchain_id,
                            chain_id,
                            store["SubChainName"],
                        )
                    )
                )

            stores.append(
                Entity(
                    ParserUtils.create_store(
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


class ParserBinaProjects(BaseParser):

    def parse_items_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_promos_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> list[Entity]:
        pass

    def parse_stores_file(
        self, file: DataFile, data: dict, server_type: SERVER_TYPE, chain_id: str
    ) -> tuple[list[Entity], list[Entity]]:
        subchain_list = data["Root"]["SubChains"]["SubChain"]
        if isinstance(subchain_list, dict):
            subchain_list = [subchain_list]

        subchains = []
        stores = []

        for subchain in subchain_list:
            subchains.append(
                Entity(
                    ParserUtils.create_subchain(
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
                        ParserUtils.create_store(
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


class Parser:
    def __init__(self) -> None:
        self.parsers = {
            SERVER_TYPE.Cerberus: ParserCerberus(),
            SERVER_TYPE.Shufersal: ParserShufersal(),
            SERVER_TYPE.SuperPharm: ParserSuperPharm(),
            SERVER_TYPE.Nibit: ParserNibit(),
            SERVER_TYPE.BinaProjects: ParserBinaProjects(),
        }

    def parse(self, file: DataFile) -> list[Entity] | tuple[list[Entity], list[Entity]]:
        """Returns all the entities in the file."""
        if file.content is None:
            return ([], [])

        data = xmltodict.parse(file.content)
        server_type = CHAINS_DATA[file.chain]["server"]["type"]
        chain_id = CHAINS_DATA[file.chain]["id"]

        parser: BaseParser = self.parsers[server_type]
        match FILE_CATEGORY_TO_ENTITY_TYPE[file.category]:
            case ENTITY_TYPE.Item:
                return parser.parse_items_file(file, data, server_type, chain_id)
            case ENTITY_TYPE.Promo:
                return parser.parse_promos_file(file, data, server_type, chain_id)
            case ENTITY_TYPE.Store:
                return parser.parse_stores_file(file, data, server_type, chain_id)
            case _:
                raise Exception("Invalid entity type")


class ParserUtils:
    @staticmethod
    def create_store(
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
            "id": ParserUtils.normalize_number(id),
            "chain_id": chain_id,
            "subchain_id": ParserUtils.normalize_number(subchain_id),
            "bikoret_number": ParserUtils.normalize_number(bikoret_number)[0],
            "type": STORE_TYPE[ParserUtils.normalize_number(type)],
            "name": name or "",
            "address": address or "",
            "city": city or "",
            "zip_code": ParserUtils.normalize_number(zip_code),
        }

    @staticmethod
    def create_subchain(id: str, chain_id: str, name: str) -> dict:
        return {
            "id": ParserUtils.normalize_number(id),
            "chain_id": chain_id,
            "name": name or "",
        }

    @staticmethod
    def normalize_number(number: str) -> str:
        try:
            return str(int(number))
        except:
            return ""


if __name__ == "__main__":
    servers = {server_type: FileServer(server_type) for server_type in SERVER_TYPE}
    store_files = {
        chain: servers[CHAINS_DATA[chain]["server"]["type"]].get_files(
            chain=chain, category=FILE_CATEGORY.Stores, amount=1
        )
        for chain in CHAIN
    }

    subchains = []
    stores = []
    parser = Parser()
    with Database() as db:
        for file_list in store_files.values():
            if len(file_list) > 0:
                curr_subchains, curr_stores = parser.parse(file_list[0])
                subchains.extend(curr_subchains)
                stores.extend(curr_stores)

        db.insert_entities(TABLE.Subchain, subchains)
        db.insert_entities(TABLE.Store, stores)

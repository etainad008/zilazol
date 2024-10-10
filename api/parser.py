from abc import ABC, abstractmethod
import xmltodict
from collections import defaultdict
import json

from entity import Entity
from constants import *
from data_file import DataFile
from file_server import FileServer
from process import derive_name, normalize_whitespace


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
    ) -> list[dict]:
        root = data.get("Root", data.get("root"))
        item_list = root["Items"]["Item"]
        subchain_id = root["SubChainId"]
        store_id = root["StoreId"]

        return [
            ParserUtils.create_item(
                chain_id,
                subchain_id,
                store_id,
                item["ItemCode"],
                item["ItemType"],
                item["ItemName"],
                item["ManufacturerName"],
                item["ManufactureCountry"],
                item["ManufacturerItemDescription"],
                item["UnitQty"],
                item["Quantity"],
                item["bIsWeighted"],
                item["UnitOfMeasure"],
                item["UnitOfMeasurePrice"],
                item["QtyInPackage"],
                item["ItemStatus"],
                item["ItemPrice"],
                item["AllowDiscount"],
            )
            for item in item_list
        ]

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
        root = data.get("Root", data.get("root"))
        item_list = root["Items"]["Item"]
        subchain_id = root["SubChainId"]
        store_id = root["StoreId"]

        return [
            ParserUtils.create_item(
                chain_id,
                subchain_id,
                store_id,
                item["ItemCode"],
                item["ItemType"],
                item["ItemName"],
                item["ManufacturerName"],
                item["ManufactureCountry"],
                item["ManufacturerItemDescription"],
                item["UnitQty"],
                item["Quantity"],
                item["bIsWeighted"],
                item["UnitOfMeasure"],
                item["UnitOfMeasurePrice"],
                item["QtyInPackage"],
                item["ItemStatus"],
                item["ItemPrice"],
                item["AllowDiscount"],
            )
            for item in item_list
        ]

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

    def parse(
        self, file: DataFile
    ) -> list[Entity] | tuple[list[Entity], list[Entity]] | list[dict]:
        """Returns all the entities in the file."""
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
            "bikoret_number": ParserUtils.parse_store_bikoret_number(bikoret_number),
            "type": ParserUtils.parse_store_type(type).value,
            "name": name or "",
            "address": address or None,
            "city": city or None,
            "zip_code": ParserUtils.parse_store_zip_code(zip_code),
        }

    @staticmethod
    def create_subchain(id: str, chain_id: str, name: str) -> dict:
        return {
            "id": ParserUtils.normalize_number(id),
            "chain_id": chain_id,
            "name": name or "",
        }

    @staticmethod
    def create_item(
        chain_id: str,
        subchain_id: str,
        store_id: str,
        code: str,
        type: str,
        name: str,
        manufacturer_name: str,
        manufacture_country: str,
        manufacturer_item_description: str,
        quantity_unit: str,
        quantity: str,
        is_weighted: str,
        unit_of_measure: str,
        unit_of_measure_price: str,
        quantity_in_package: str,
        status: str,
        price: str,
        allow_discount: str,
    ):
        return {
            "chain_id": chain_id,
            "subchain_id": ParserUtils.normalize_number(subchain_id),
            "store_id": ParserUtils.normalize_number(store_id),
            "code": normalize_whitespace(code),
            "type": ParserUtils.parse_item_type(type),
            "name": normalize_whitespace(name),
            "manufacturer_name": normalize_whitespace(manufacturer_name),
            "manufacture_country": normalize_whitespace(manufacture_country),
            "manufacturer_item_description": normalize_whitespace(
                manufacturer_item_description
            ),
            "quantity_unit": ParserUtils.parse_unit(quantity_unit),
            "quantity": ParserUtils.parse_decimal(quantity),
            "is_weighted": ParserUtils.parse_bool(is_weighted),
            "unit_of_measure": normalize_whitespace(unit_of_measure),
            "unit_of_measure_price": ParserUtils.parse_decimal(unit_of_measure_price),
            "quantity_in_package": ParserUtils.parse_number(quantity_in_package),
            "status": ParserUtils.parse_item_status(status),
            "price": ParserUtils.parse_decimal(price),
            "allow_discount": ParserUtils.parse_bool(allow_discount),
        }

    @staticmethod
    def parse_bool(bool: str) -> bool:
        bool = bool.strip()
        if bool == "1":
            return True

        if bool == "0":
            return False

        raise ValueError("Boolean values must be 0 or 1")

    @staticmethod
    def normalize_number(number: str) -> str | None:
        try:
            return str(int(number))
        except ValueError:
            return None

    @staticmethod
    def normalize_decimal(decimal: str) -> str | None:
        try:
            return str(float(decimal))
        except ValueError:
            return None

    @staticmethod
    def parse_store_type(type: str) -> STORE_TYPE:
        return STORE_TYPE_MAP.get(
            ParserUtils.normalize_number(type), STORE_TYPE.Physical
        )

    @staticmethod
    def parse_store_bikoret_number(bikoret_number: str) -> str:
        return ParserUtils.normalize_number(bikoret_number) or "0"

    @staticmethod
    def parse_store_zip_code(zip_code: str) -> str:
        return (
            zip_code
            if zip_code and (zip_code.isdigit() and len(zip_code) == 7)
            else None
        )

    @staticmethod
    def parse_item_type(type: str) -> ITEM_TYPE:
        match ParserUtils.normalize_number(type):
            case "0":
                return ITEM_TYPE.Proprietary
            case "1":
                return ITEM_TYPE.Normal

        return ITEM_TYPE.Normal

    @staticmethod
    def parse_item_status(status: str) -> ITEM_STATUS:
        match ParserUtils.normalize_number(status):
            case ITEM_STATUS.Updated:
                return ITEM_STATUS.Updated
            case ITEM_STATUS.Removed:
                return ITEM_STATUS.Removed
            case ITEM_STATUS.Added:
                return ITEM_STATUS.Added
            case _:
                return ITEM_STATUS.Updated

    @staticmethod
    def parse_unit(unit: str) -> UNIT:
        match unit:
            case "גרמים" | "גרם" | "גר" | "ג":
                return UNIT.Gram
            case "Unknown" | "לא ידוע" | "לא מנהל יחידת מידה":
                return UNIT.Unknown
            case "מיליליטרים" | "מיל" | "מיליליטר" | "מל" | 'מ"ל' | "מ'ל":
                return UNIT.Milliliter
            case "ליטרים" | "ליטר" | "ל":
                return UNIT.Liter
            case "קילוגרמים" | "קילוגרם" | "קילו" | "ק'ג" | 'ק"ג':
                return UNIT.Kilogram
            case "יחידות" | "יחידה" | "יח'" | "יח" | 'י"ח' | "י'ח":
                return UNIT.Unit
            case "מטרים":
                return UNIT.Meter

        if "יח" in unit:
            return UNIT.Unit

        return UNIT.Unit

    @staticmethod
    def parse_number(number: str) -> int:
        try:
            return int(ParserUtils.normalize_number(number))
        except:
            return None

    @staticmethod
    def parse_decimal(decimal: str) -> float:
        try:
            return float(ParserUtils.normalize_decimal(decimal))
        except:
            return None


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name  # or obj.value if you prefer
        return super().default(obj)


def enum_decoder(dct):
    for key, value in dct.items():
        if isinstance(value, str):  # Check if the value is a string
            # Check which enum it belongs to and decode it
            for e in [
                CHAIN,
                SERVER_TYPE,
                FILE_CATEGORY,
                ENTITY_TYPE,
                TABLE,
                UNIT,
                STORE_TYPE,
                ITEM_TYPE,
                ITEM_STATUS,
            ]:
                try:
                    dct[key] = e[value]  # Add more Enums as needed
                except KeyError:
                    pass  # If the value doesn't match an Enum member, keep it as is
    return dct


if __name__ == "__main__":
    servers = {server_type: FileServer(server_type) for server_type in SERVER_TYPE}
    price_files = {
        chain: servers[CHAINS_DATA[chain]["server"]["type"]].get_files(
            chain=chain, category=FILE_CATEGORY.PricesFull, amount=1
        )
        for chain in CHAIN
        if CHAINS_DATA[chain]["server"]["type"] == SERVER_TYPE.Shufersal
    }

    parser = Parser()
    a = parser.parse(price_files[CHAIN.Shufersal][0])

    pass

    # price_files = {}
    # for chain in CHAIN:
    #     if chain in [CHAIN.HaziHinam]:
    #         continue

    #     print(f"Fetching data from {chain}...")

    #     price_files[chain] = servers[CHAINS_DATA[chain]["server"]["type"]].get_files(
    #         chain=chain, category=FILE_CATEGORY.PricesFull, amount=1
    #     )

    #     print(f"Finished fetching data from {chain}.")

    # items_dict = defaultdict(list)
    # parser = Parser()

    # for chain in price_files:
    #     print(f"Parsing {chain}...")

    #     try:
    #         for file in price_files[chain]:
    #             items = parser.parse(file)
    #             for item in items:
    #                 items_dict[item["code"]].append(item)
    #     except:
    #         pass

    #     print(f"Finished parsing {chain}")

    # items_dict = {code: l for code, l in items_dict.items() if len(l) > 3}

    # print("Parsed!")

    # with open("output.json", "w", encoding="utf-8") as file:
    #     json.dump(items_dict, file, cls=EnumEncoder, ensure_ascii=False, indent=4)

    # with open(r"D:\projects\zilazol\output.json", "r", encoding="utf-8") as file:
    #     items_dict = json.load(file, object_hook=enum_decoder)

    # print("Parsed")

    # count = 0
    # print(f"Parsing {len(items_dict)} items.")
    # for code in items_dict:
    #     derived_name = derive_name([item["name"] for item in items_dict[code]])
    #     count += 1
    #     if count % 25 == 0:
    #         print(f"{count}... {code} : {derived_name}")

    # print("\nDone")

    # with Database() as db:
    #     for file_list in store_files.values():
    #         if len(file_list) > 0:
    #             curr_subchains, curr_stores = parser.parse(file_list[0])
    #             subchains.extend(curr_subchains)
    #             stores.extend(curr_stores)

    #     db.insert_entities(TABLE.Subchain, subchains)
    #     db.insert_entities(TABLE.Store, stores)

    # a = servers[SERVER_TYPE.BinaProjects].get_files(
    #     chain=CHAIN.SuperYoda, category=FILE_CATEGORY.Stores, amount=1
    # )

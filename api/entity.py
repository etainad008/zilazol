from abc import ABC, abstractmethod
from datetime import datetime

from constants import *


class Entity(ABC):
    """An entity. This can be an item, a promotion or a store."""

    def __new__(
        cls, type: ENTITY_TYPE, server_type: SERVER_TYPE, data: dict
    ) -> "Entity":
        match type:
            case ENTITY_TYPE.Item:
                return super().__new__(Item)
            case ENTITY_TYPE.Promo:
                return super().__new__(Promotion)
            case ENTITY_TYPE.Store:
                return super().__new__(Store)
            case _:
                raise ValueError(f"Unsupported entity type: {type}")

    def __init__(self, type: ENTITY_TYPE, server_type: SERVER_TYPE, data: dict) -> None:
        self.type = type
        self.server_type = server_type
        self.data = data

        self.format = Entity.get_entity_format(type, server_type)

        # TODO: maybe we can just use the "get" method when needed
        #       instead of initializing everything?
        match self.type:
            case ENTITY_TYPE.Item:
                self.update_date = self.get("update_date")
                self.item_code = self.get("item_code")
                self.item_type = self.get("item_type")
                self.item_name = self.get("item_name")
                self.manufacturer_name = self.get("manufacturer_name")
                self.manufacture_country = self.get("manufacture_country")
                self.manufacturer_item_description = data[
                    self.format["manufacturer_item_description"]
                ]
                self.unit_quantity = self.get("unit_quantity")
                self.quantity = self.get("quantity")
                self.b_is_weighted = self.get("b_is_weighted")
                self.unit_of_measurement = self.get("unit_of_measurement")
                self.quantity_in_package = self.get("quantity_in_package")
                self.item_price = self.get("item_price")
                self.unit_of_measurement_price = data[
                    self.format["unit_of_measurement_price"]
                ]
                self.allow_discount = self.get("allow_discount")
                self.item_status = self.get("item_status")

            case ENTITY_TYPE.Promo:
                self.promotion_id = self.get("promotion_id")
                self.promotion_description = self.get("promotion_description")
                self.promotion_update_date = self.get("promotion_update_date")
                self.allow_multiple_discounts = self.get("allow_multiple_discounts")
                self.promotion_start_date = self.get("promotion_start_date")
                self.promotion_start_hour = self.get("promotion_start_hour")
                self.promotion_end_date = self.get("promotion_end_date")
                self.promotion_end_hour = self.get("promotion_end_hour")
                self.min_quantity = self.get("min_quantity")
                self.reward_type = self.get("reward_type")
                self.discounted_price = self.get("discounted_price")
                self.min_number_of_item_offered = data[
                    self.format["min_number_of_item_offered"]
                ]
                self.promotion_items = self.get("promotion_items")
                self.additional_restrictions = self.get("additional_restrictions")
                self.clubs = self.get("clubs")

            case ENTITY_TYPE.Store:
                self.chain_id = self.get("chain_id")
                self.store_id = self.get("store_id")
                self.store_name = self.get("store_name")
                self.store_type = self.get("store_type")
                self.chain = self.get("chain")
                self.bikoret_number = self.get("bikoret_number")
                self.subchain_id = self.get("subchain_id")
                self.subchain_name = self.get("subchain_name")
                self.city = self.get("city")
                self.address = self.get("address")
                self.zipcode = self.get("zipcode")

    def get(self, field: str):
        return self.data.get(self.format[field], None)

    @staticmethod
    def get_entity_format(type: ENTITY_TYPE, server_type: SERVER_TYPE):
        return SERVER_TYPE_DATA[server_type]["categories"][
            ENTITY_TYPE_TO_FILE_CATEGORY[type]
        ]["format"]["entity"]

    @staticmethod
    def parse_datetime(date: str, time: str) -> datetime:
        return datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")


class Item(Entity):
    pass


class Promotion(Entity):
    pass


class Store(Entity):
    pass

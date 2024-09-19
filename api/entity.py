from abc import ABC, abstractmethod
from datetime import datetime

from constants import *


class Entity(ABC):
    """An entity. This can be an item, a promotion or a store."""

    def __new__(cls, type: ENTITY_TYPE, data: dict) -> "Entity":
        match type:
            case ENTITY_TYPE.Item:
                return super().__new__(Item)
            case ENTITY_TYPE.Promo:
                return super().__new__(Promotion)
            case ENTITY_TYPE.Store:
                return super().__new__(Store)
            case _:
                raise ValueError(f"Unsupported entity type: {type}")

    def __init__(self, type: ENTITY_TYPE, data: dict) -> None:
        match type:
            case ENTITY_TYPE.Item:
                self.name = data["ItemName"]  # the name of the item
                self.code = data["ItemCode"]  # the code of the item (maka"t)
                self.price = data["ItemPrice"]  # the price of the item (in Shekels)
                self.unit = data[
                    "UnitQty"
                ]  # the unit used to measure the item's quantity
                self.quantity = data["Quantity"]  # the quantity of the item
            case ENTITY_TYPE.Promo:
                self.id = data["PromotionId"]
                self.description = data["PromotionDescription"]
                self.start = self.parse_datetime(
                    data["PromotionStartDate"], data["PromotionStartHour"]
                )
                self.end = self.parse_datetime(
                    data["PromotionEndDate"], data["PromotionEndHour"]
                )
                self.remark = data["Remark"]
                self.items = data["PromotionItems"]["Item"]
            case ENTITY_TYPE.Store:
                self.id = data["StoreId"]
                self.name = data["StoreName"]
                self.address = data["Address"]
                self.city = data["City"]
                self.zip_code = data["ZipCode"]


class Item(Entity):
    pass


class Promotion(Entity):
    @staticmethod
    def parse_datetime(date: str, time: str) -> datetime:
        return datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")


class Store(Entity):
    pass

from constants import *
from entity import Entity
import xmltodict


class DataFile:
    def __init__(
        self, content: bytes, category: FILE_CATEGORY, server_type: SERVER_TYPE
    ) -> None:
        self.content = content
        self.category = category
        self.server_type = server_type
        self.format = SERVER_TYPE_DATA[server_type]["categories"][category]["format"]

    def parse(self) -> list[Entity]:
        data_dict = xmltodict.parse(self.content, encoding="utf-8")
        entity_list_path = (
            self.format["root"] + " " + self.format["entity_list"]
        ).split(" ")

        # traverse the dict to get the entity list
        entity_list = data_dict
        for node in entity_list_path:
            entity_list = entity_list[node]

        return [
            Entity(type=FILE_CATEGORY_TO_ITEM_TYPE[self.category], data=entity)
            for entity in entity_list
        ]

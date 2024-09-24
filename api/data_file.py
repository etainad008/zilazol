from constants import (
    FILE_CATEGORY,
    SERVER_TYPE,
    SERVER_TYPE_DATA,
    FILE_CATEGORY_TO_ENTITY_TYPE,
)
from entity import Entity
import xmltodict


class DataFile:
    def __init__(
        self, content: bytes, category: FILE_CATEGORY, server_type: SERVER_TYPE
    ) -> None:
        self.content = content
        self.category = category
        self.server_type = server_type
        self.file_format = SERVER_TYPE_DATA[server_type]["categories"][category][
            "format"
        ]["file"]
        self.entity_format = SERVER_TYPE_DATA[server_type]["categories"][category][
            "format"
        ]["entity"]

    def parse(self) -> list[Entity]:
        data_dict = xmltodict.parse(self.content, encoding="utf-8")

        # traverse the dict to get the entity list
        entity_list = self.get_value_by_path(
            data_dict,
            self.build_path(self.file_format["root"], self.file_format["entity_list"]),
        )

        return [
            Entity(
                type=FILE_CATEGORY_TO_ENTITY_TYPE[self.category],
                server_type=self.server_type,
                data=entity,
            )
            for entity in entity_list
        ]

    def get_value_by_path(self, data: dict, path: str):
        value = data
        for temp in path:
            value = value[temp]

        return value

    def build_path(self, *args) -> str:
        return (" ".join(args)).split(" ")

class Entity:
    """An entity. This can be an item, a promotion a store a subchain, or a chain."""

    def __init__(self, data: dict) -> None:
        self.data = data

    def __len__(self):
        return len(self.data)

    def to_value_tuple(self):
        return tuple(i for i in self.data.values())

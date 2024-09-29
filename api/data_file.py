from constants import FILE_CATEGORY, SERVER_TYPE, CHAIN


class DataFile:
    def __init__(
        self,
        content: bytes,
        chain: CHAIN,
        category: FILE_CATEGORY,
    ) -> None:
        self.content = content
        self.chain = chain
        self.category = category

from constants import *
from file_server import FileServer


class Chain:
    """Represents a chain. Includes the chain's server."""

    def __init__(self, chain: CHAIN):
        chain_data = CHAINS_DATA[chain]

        self.chain = chain
        self.id = chain_data["id"]
        self.server = FileServer(
            type=chain_data["server"]["type"], creds=chain_data["server"]["creds"]
        )

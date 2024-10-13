from constants import CHAINS_DATA
from database import Database


def populate():
    populate_chains()


def populate_chains():
    values = [(CHAINS_DATA[chain]["id"], chain.name) for chain in CHAINS_DATA.keys()]
    with Database() as db:
        db.execute_many(
            """
            INSERT INTO Chain VALUES (%s, %s);
            """,
            values,
        )


if __name__ == "__main__":
    populate()

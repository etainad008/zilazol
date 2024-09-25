# i love my dad
import psycopg
from os import environ


class Database:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = psycopg.connect(
            dbname="zilazol",
            user="postgres",
            password=environ.get("POSTGRES_PASSWORD"),
            host="localhost",
            port="5432",
        )
        self.cursor = self.connection.cursor()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.cursor.closed:
            self.cursor.close()

        if not self.connection.closed:
            self.connection.close()

        return False  # dont suppress exceptions

    def commit(self):
        self.connection.commit()

    def execute(self, query: str, *, commit: bool = True):
        self.cursor.execute(query=query)
        if commit:
            self.commit()

    def execute_many(self, query: str, iterable, *, commit: bool = True):
        self.cursor.executemany(query=query, params_seq=iterable)
        if commit:
            self.commit()

    def get_rows(self, amount: int = -1) -> list | None:
        if amount == -1:
            return self.cursor.fetchall()

        if amount == 1:
            return self.cursor.fetchone()

        return self.cursor.fetchmany(amount)

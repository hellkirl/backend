from dataclasses import dataclass

import psycopg2  # type: ignore


@dataclass
class Connector:
    """This class is used to create a connector to PostgreSQL"""

    database: str
    username: str
    password: str
    port: int = 5432

    def connect(self) -> tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor] | None:
        """
        This method makes connection with migrations
        :return: tuple with connector ad cursor
        """
        try:
            con = psycopg2.connect(database=self.database, user=self.username, password=self.password, port=self.port)
            cur = con.cursor()
            con.set_session(autocommit=True)
            return con, cur
        except Exception as connection_error:
            print(f"The error is: {str(connection_error)}")
            return None

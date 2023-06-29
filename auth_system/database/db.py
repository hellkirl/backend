import getpass
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
        This method makes connection with database
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


if __name__ == "__main__":
    database, username, password, port = (
        input("Enter the name of the database: "),
        input("Enter your username: "),
        getpass.getpass(),
        int(input("Enter port to the database: ")),
    )
    try:
        c = Connector(database=database, username=username, password=password, port=port)
        conn, curs = c.connect()  # type: ignore
        curs.execute(
            """CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR (255),
            last_name VARCHAR (255),
            email VARCHAR (322),
            phone VARCHAR (15),
            login VARCHAR (255),
            password VARCHAR)"""
        )
        conn.close()
        curs.close()
        print("The table 'users' was successfully created")
    except Exception as structure_error:
        print(f"Your error is: {str(structure_error)}")
    finally:
        print("Connection to the database is closed")

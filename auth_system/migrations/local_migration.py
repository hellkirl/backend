from auth_system.config import DATABASE, PASSWORD, PORT, USERNAME  # type: ignore
from db import Connector


def local_schema(database: str, username: str, pwd: str, port: int = 5432) -> None:
    """
    The function locally creates a table 'users'
    :param database: name of db
    :param username: login
    :param pwd: password
    :param port: used port for db
    :return: None
    """
    try:
        c = Connector(database=database, username=username, password=pwd, port=port)
        con, cur = c.connect()  # type: ignore
        cur.execute(
            """CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR (255),
            last_name VARCHAR (255),
            email VARCHAR (322),
            phone VARCHAR (15),
            password VARCHAR)"""
        )
        con.close()
        cur.close()
        print("The table 'users' was successfully created")
    except TypeError as NoneTypeError:
        print(f"Your error is: {NoneTypeError}. Make sure your database is active.")
        with open("report.txt", "w") as error_file:
            error_file.write(str(NoneTypeError))
    except Exception as migrations_error:
        print(f"Your error is: {migrations_error}.")
        with open("error.txt", "w") as error_file:
            error_file.write(str(migrations_error))
    finally:
        print("Connection to the database is closed")


if __name__ == "__main__":
    local_schema(DATABASE, USERNAME, PASSWORD, PORT)

from db import Connector

from auth_system.config import DATABASE, PASSWORD, PORT, USERNAME

if __name__ == "__main__":
    try:
        if not PORT:
            PORT = 5432
        c = Connector(database=DATABASE, username=USERNAME, password=PASSWORD, port=PORT)
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
        print("Connection to the migrations is closed")

from config import DATABASE, PASSWORD, PORT, USERNAME
from migrations.db import Connector  # type: ignore
from pydantic.dataclasses import dataclass

c = Connector(database=DATABASE, username=USERNAME, password=PASSWORD, port=PORT)
con, cur = c.connect()


@dataclass
class User:
    first_name: str
    last_name: str
    login: str
    password: str
    email: str
    phone_number: str

    def create(self):
        try:
            cur.execute(
                """INSERT INTO users (first_name, last_name, email, phone_number, login, password)
                                        VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    self.first_name,
                    self.last_name,
                    self.email,
                    self.phone_number,
                    self.login,
                    self.password,
                ),
            )
        except Exception as error:
            print(
                f"It is not possible to create a new user because of the following error {str(error)}"
            )
            con.rollback()

    def check(self):
        cur.execute("SELECT * FROM users WHERE email = %s", (self.email,))
        if cur.fetchone() is None:
            return True
        else:
            return False

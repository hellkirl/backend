import unittest
from unittest import mock

from auth_system.migrations.db import Connector
from auth_system.config import DATABASE, USERNAME, PASSWORD, PORT


class AuthSystemTest(unittest.TestCase):
    def test_schema(self):
        expected_columns = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "login",
            "password",
        ]

        c = Connector(DATABASE, USERNAME, PASSWORD, PORT)
        con, cur = c.connect()
        cur.execute("SELECT * FROM users LIMIT 0")
        actual_columns = [desc[0] for desc in cur.description]

        self.assertEqual(expected_columns, actual_columns)

    def test_connection(self):
        with mock.patch("psycopg2.connect") as mock_con:
            c = Connector(DATABASE, USERNAME, PASSWORD, PORT)
            c.connect()

            mock_con.assert_called_once_with(
                database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT
            )


if __name__ == "__main__":
    unittest.main()

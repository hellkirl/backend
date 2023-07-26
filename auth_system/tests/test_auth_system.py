import unittest
from unittest import mock
from unittest.mock import call

import psycopg2

from auth_system.migrations.db import Connector
from auth_system.models import User


class AuthSystemTest(unittest.TestCase):
    def test_schema(self):
        columns = ("id", "first_name", "last_name", "email", "phone", "login", "password")

    def test_connection(self):
        ...

    def test_new_user(self):
        ...


if __name__ == "__main__":
    unittest.main()

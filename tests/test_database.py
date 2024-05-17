import unittest
from database.connection import get_engine, test_connection

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """
        Set up a test database engine. Here, we use an SQLite in-memory database for simplicity.
        """
        self.sqlite_engine = get_engine('sqlite', '', '', '', '', ':memory:')
        # You can add other database engines here for different database types
        self.postgresql_engine = get_engine('postgresql', 'localhost', '5432', 'username', 'password', 'test_db')
        self.mysql_engine = get_engine('mysql', 'localhost', '3306', 'username', 'password', 'test_db')
        self.mssql_engine = get_engine('mssql', 'localhost', '1433', 'username', 'password', 'test_db')
        self.oracle_engine = get_engine('oracle', 'localhost', '1521', 'username', 'password', 'test_db')

    def test_sqlite_connection(self):
        """
        Test connection to an SQLite database.
        """
        self.assertTrue(test_connection(self.sqlite_engine), "SQLite database connection failed")

    def test_postgresql_connection(self):
        """
        Test connection to a PostgreSQL database.
        """
        self.assertTrue(test_connection(self.postgresql_engine), "PostgreSQL database connection failed")

    def test_mysql_connection(self):
        """
        Test connection to a MySQL database.
        """
        self.assertTrue(test_connection(self.mysql_engine), "MySQL database connection failed")

    def test_mssql_connection(self):
        """
        Test connection to a MSSQL database.
        """
        self.assertTrue(test_connection(self.mssql_engine), "MSSQL database connection failed")

    def test_oracle_connection(self):
        """
        Test connection to an Oracle database.
        """
        self.assertTrue(test_connection(self.oracle_engine), "Oracle database connection failed")

if __name__ == '__main__':
    unittest.main()

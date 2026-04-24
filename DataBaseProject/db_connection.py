import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    """
    Singleton class to manage MySQL database connection
    """
    _instance = None
    _connection = None

    def __new__(cls, host, user, password, database):
        """
        Override new method to ensure only one instance of the class
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            try:
                cls._connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                if cls._connection.is_connected():
                    print("Database connection successful")
            except Error as e:
                print(f"Error connecting to database: {e}")
                cls._connection = None
        return cls._instance

    @classmethod
    def get_connection(cls):
        """
        Return the connection object
        """
        if cls._connection is not None and cls._connection.is_connected():
            return cls._connection
        else:
            print("Database connection is not active.")
            return None

    @classmethod
    def close_connection(cls):
        """
        Close the database connection
        """
        if cls._connection is not None and cls._connection.is_connected():
            cls._connection.close()
            print("Database connection closed")

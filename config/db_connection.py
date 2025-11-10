import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


class DatabaseConnection:
    def __init__(self):
        load_dotenv()

        self.host = os.getenv("DB_HOST", "127.0.0.1")
        self.port = os.getenv("DB_PORT", "3306")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "db_projeto_catalogo")

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if connection.is_connected():
                return connection

        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def close_connection(self, connection):
        try:
            if connection and connection.is_connected():
                connection.close()
        except Error as e:
            print(f"Erro ao encerrar a conexão: {e}")

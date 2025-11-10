# Arquivo para testar a conexão com o banco de dados

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.db_connection import DatabaseConnection
import os

db = DatabaseConnection()
print("Host:", db.host)
print("Port:", db.port)
print("User:", db.user)
print("DB:", db.database)


conn = db.get_connection()

if conn:
    print("Conexão realizada com sucesso!")
    db.close_connection(conn)
else:
    print("Erro ao tentar conectar.")

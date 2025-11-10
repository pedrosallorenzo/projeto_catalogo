# Arquivo principal para executar o app

from config.db_connection import DatabaseConnection
from model.midia import MidiaModel
from controller.midia_controller import MidiaController
from view.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow(MidiaController(MidiaModel(DatabaseConnection())))
    app.mainloop()

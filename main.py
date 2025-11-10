from config.db_connection import DatabaseConnection
from model.midia import MidiaModel
from controller.midia_controller import MidiaController
from view.main_window import CTKApp

if __name__ == "__main__":
    app = CTKApp(MidiaController(MidiaModel(DatabaseConnection())))
    app.mainloop()

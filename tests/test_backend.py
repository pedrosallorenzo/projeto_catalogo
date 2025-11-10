from config.db_connection import DatabaseConnection
from model.midia import MidiaModel, Midia
from controller.midia_controller import MidiaController

db = DatabaseConnection()
model = MidiaModel(db)
ctl = MidiaController(model)

print(ctl.adicionar("Avatar", "filme", "Ficção", "2009", "assistido", "9"))
print(ctl.adicionar("Breaking Bad", "serie", "Crime", "2008", "pendente", ""))

print(ctl.listar_todas())

print(ctl.filtrar(status="pendente"))
print(ctl.filtrar(titulo_like="a", nota_op=">=", nota_val="8"))

print(ctl.atualizar_status_nota(id_midia="1", status="assistido", nota="10"))

print(ctl.excluir("99999"))

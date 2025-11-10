from typing import Optional, Dict, Any
from model.midia import Midia, MidiaModel, TIPOS_VALIDOS, STATUS_VALIDOS


class MidiaController:
    def __init__(self, model: MidiaModel):
        self.model = model

    # Função para criar (CREATE)
    def adicionar(
        self,
        titulo: str,
        tipo: str,
        genero: Optional[str] = None,
        ano: Optional[str] = None,
        status: str = "pendente",
        nota: Optional[str] = None,
    ) -> Dict[str, Any]:

        # Algumas validações
        if not titulo or not titulo.strip():
            return {"ok": False, "msg": "Título é obrigatório."}
        tipo = (tipo or "").strip().lower()
        if tipo not in TIPOS_VALIDOS:
            return {"ok": False, "msg": "Tipo inválido. Use 'filme' ou 'serie'."}

        status = (status or "").strip().lower() or "pendente"
        if status not in STATUS_VALIDOS:
            return {
                "ok": False,
                "msg": "Status inválido. Use 'pendente' ou 'assistido'.",
            }

        ano_int = None
        if ano not in (None, "", "None"):
            try:
                ano_int = int(ano)
                if not (1878 <= ano_int <= 2100):  # 1878 ~ primeira filmagem
                    return {"ok": False, "msg": "Ano fora do intervalo válido."}
            except ValueError:
                return {"ok": False, "msg": "Ano deve ser numérico."}

        nota_int = None
        if nota not in (None, "", "None"):
            try:
                nota_int = int(nota)
                if not (0 <= nota_int <= 10):
                    return {"ok": False, "msg": "Nota deve estar entre 0 e 10."}
            except ValueError:
                return {"ok": False, "msg": "Nota deve ser numérica."}

        m = Midia(
            titulo=titulo.strip(),
            tipo=tipo,
            genero=(genero or None),
            ano=ano_int,
            status=status,
            nota=nota_int,
        )
        ok, msg, new_id = self.model.create(m)
        return {"ok": ok, "msg": msg, "data": new_id}

    # Função para listar (READ)
    def listar_todas(self) -> Dict[str, Any]:
        ok, msg, itens = self.model.list_all()
        return {"ok": ok, "msg": msg, "data": itens}

    def filtrar(
        self,
        titulo_like: Optional[str] = None,
        genero: Optional[str] = None,
        status: Optional[str] = None,
        tipo: Optional[str] = None,
        ano: Optional[str] = None,
        nota_ordem=None,
    ) -> Dict[str, Any]:

        ano_int = None
        if ano not in (None, "", "None"):
            try:
                ano_int = int(ano)
            except ValueError:
                return {"ok": False, "msg": "Ano do filtro deve ser numérico."}

        if tipo:
            tipo = tipo.strip().lower()
            if tipo not in TIPOS_VALIDOS:
                return {"ok": False, "msg": "Tipos do filtro inválidos."}

        # nota
        if nota_ordem:
            nota_ordem = nota_ordem.lower()
            if nota_ordem not in ("asc", "desc"):
                return {"ok": False, "msg": "Ordenação inválida. Use 'asc' ou 'desc'."}

        if status:
            status = status.strip().lower()
            if status not in STATUS_VALIDOS:
                return {"ok": False, "msg": "Status do filtro inválido."}

        ok, msg, itens = self.model.filter(
            titulo_like=(titulo_like or None),
            genero=(genero or None),
            status=(status or None),
            tipo=(tipo or None),
            ano=ano_int,
            nota_ordem=nota_ordem,
        )
        return {"ok": ok, "msg": msg, "data": itens}

    # Função para atualizar (UPDATE)
    def atualizar_status_nota(
        self, id_midia: str, status: Optional[str] = None, nota: Optional[str] = None
    ) -> Dict[str, Any]:

        try:
            _id = int(id_midia)
        except (TypeError, ValueError):
            return {"ok": False, "msg": "ID inválido."}

        st = None
        if status not in (None, "", "None"):
            st = status.strip().lower()
            if st not in STATUS_VALIDOS:
                return {"ok": False, "msg": "Status inválido."}

        nt = None
        if nota not in (None, "", "None"):
            try:
                nt = int(nota)
                if not (0 <= nt <= 10):
                    return {"ok": False, "msg": "Nota deve estar entre 0 e 10."}
            except ValueError:
                return {"ok": False, "msg": "Nota deve ser numérica."}

        ok, msg = self.model.update_status_nota(_id, st, nt)
        return {"ok": ok, "msg": msg}

    def atualizar_full(self, midia: Midia) -> Dict[str, Any]:
        # Validações reutilizadas
        if not midia.id_midia:
            return {"ok": False, "msg": "ID é obrigatório."}
        if not midia.titulo or not midia.titulo.strip():
            return {"ok": False, "msg": "Título é obrigatório."}
        if midia.tipo not in TIPOS_VALIDOS:
            return {"ok": False, "msg": "Tipo inválido."}
        if midia.status not in STATUS_VALIDOS:
            return {"ok": False, "msg": "Status inválido."}
        if midia.nota is not None and not (0 <= midia.nota <= 10):
            return {"ok": False, "msg": "Nota deve estar entre 0 e 10."}
        if midia.ano is not None and not (1878 <= midia.ano <= 2100):
            return {"ok": False, "msg": "Ano fora do intervalo válido."}

        ok, msg = self.model.update_full(midia)
        return {"ok": ok, "msg": msg}

    # Função para excluir (DELETE)
    def excluir(self, id_midia: str) -> Dict[str, Any]:
        try:
            _id = int(id_midia)
        except (TypeError, ValueError):
            return {"ok": False, "msg": "ID inválido."}

        ok, msg = self.model.delete(_id)
        return {"ok": ok, "msg": msg}

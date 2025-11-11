from dataclasses import dataclass
from typing import Optional, List, Tuple, Any, Dict
from mysql.connector import Error
from config.db_connection import DatabaseConnection

TIPOS_VALIDOS = {"filme", "serie"}
STATUS_VALIDOS = {"pendente", "assistido"}


# Classe que cria as opções do usuário (propriedades)
@dataclass
class Midia:
    id_midia: Optional[int] = None
    titulo: str = ""
    tipo: str = ""
    genero: Optional[str] = None
    ano: Optional[int] = None
    status: str = "pendente"
    nota: Optional[int] = None


# Classe que junta as propriedades com as colunas do banco de dados
class MidiaModel:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def _row_to_midia(self, row: Tuple[Any, ...]) -> Midia:
        return Midia(
            id_midia=row[0],
            titulo=row[1],
            tipo=row[2],
            genero=row[3],
            ano=row[4],
            status=row[5],
            nota=row[6],
        )

    # Retorna todas as linhas da consulta
    def _fetchall_as_midias(self, cursor) -> List[Midia]:
        rows = cursor.fetchall()
        return [self._row_to_midia(r) for r in rows]

    # Função para criar / adicionar novas mídias
    def create(self, midia: Midia) -> Tuple[bool, str, Optional[int]]:
        conn = self.db.get_connection()
        if not conn:
            return (False, "Falha na conexão com o banco.", None)

        try:
            sql = """
                INSERT INTO tb_midia (titulo, tipo, genero, ano, status, nota)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        midia.titulo.strip(),
                        midia.tipo,
                        midia.genero.strip() if midia.genero else None,
                        midia.ano,
                        midia.status,
                        midia.nota,
                    ),
                )
                conn.commit()
                return (True, "Midia cadastrada com sucesso!", cur.lastrowid)
        except Error as e:
            if getattr(e, "errno", None) == 1062:
                return (False, "Já existe uma mídia com mesmo título/ano/tipo.", None)
            return (False, f"Erro ao inserir mídia: {e}", None)
        finally:
            self.db.close_connection(conn)

    # Função para filtrar todos os ítens
    def list_all(self) -> Tuple[bool, str, List[Midia]]:
        conn = self.db.get_connection()
        if not conn:
            return (False, "Falha na conexão com o banco.", [])
        try:
            sql = """
                SELECT id_midia, titulo, tipo, genero, ano, status, nota
                FROM tb_midia
                ORDER BY created_at DESC, id_midia DESC
            """
            with conn.cursor() as cur:
                cur.execute(sql)
                midias = self._fetchall_as_midias(cur)
                return (True, "Consulta realizada com sucesso!", midias)
        except Error as e:
            return (False, f"Erro ao consultar: {e}", [])
        finally:
            self.db.close_connection(conn)

    # Função para filtrar os ítens específicos
    def filter(
        self,
        titulo_like: Optional[str] = None,
        genero: Optional[str] = None,
        status: Optional[str] = None,
        ano: Optional[int] = None,
        tipo: Optional[str] = None,
        nota_ordem: Optional[str] = None,
    ) -> Tuple[bool, str, List[Midia]]:
        conds: List[str] = []
        params: List = []

        if titulo_like:
            conds.append("titulo LIKE %s")
            params.append(f"%{titulo_like}%")
        if genero:
            conds.append("genero LIKE %s")
            params.append(f"%{genero}%")
        if status:
            conds.append("status = %s")
            params.append(status)
        if tipo:
            conds.append("tipo = %s")
            params.append(tipo)
        if ano:
            conds.append("ano = %s")
            params.append(ano)

        order_clause = ""
        if nota_ordem:
            nota_ordem = nota_ordem.upper()
            if nota_ordem in ("CRE", "DEC"):
                conds.append("nota IS NOT NULL")
                order_clause = f" ORDER BY nota {nota_ordem}"

        where_clause = (" WHERE " + " AND ".join(conds)) if conds else ""

        sql = (
            "SELECT id_midia, titulo, tipo, genero, ano, status, nota "
            f"FROM tb_midia{where_clause}{order_clause};"
        )

        conn = self.db.get_connection()
        if not conn:
            return (False, "Falha na conexão com o banco.", [])
        try:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(sql, tuple(params))
                rows = cur.fetchall()
                itens = [Midia(**row) for row in rows]
            return (True, "Consulta realizada com sucesso!", itens)
        except Error as e:
            return (False, f"Erro ao consultar: {e}", [])
        finally:
            self.db.close_connection(conn)

    # Função que atualiza apenas o status e a nota
    def update_status_nota(
        self, id_midia: int, status: Optional[str], nota: Optional[int]
    ) -> Tuple:
        conn = self.db.get_connection()
        if not conn:
            return (False, "Falha na conexão com o banco.")

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM tb_midia WHERE id_midia = %s", (int(id_midia),)
                )
                if cur.fetchone() is None:
                    return (False, "ID não encontrado.")

            sets = []
            params: list[Any] = []
            if status is not None:
                sets.append("status = %s")
                params.append(status)
            if nota is not None:
                sets.append("nota = %s")
                params.append(nota)

            if not sets:
                return (False, "Nada para atualizar.")

            params.append(int(id_midia))
            sql = f"UPDATE tb_midia SET {', '.join(sets)} WHERE id_midia = %s"
            cur.execute(sql, tuple(params))
            conn.commit()
            if cur.rowcount == 0:
                return (True, "Nada alterado (valores iguais).")
            return (True, "Atualizado com sucesso.")
        except Error as e:
            return (False, f"Erro ao atualizar: {e}")
        finally:
            self.db.close_connection(conn)

    # Função para atualizar todos os ítens do catálogo
    def update_full(self, midia: Midia) -> Tuple[bool, str]:
        if not midia.id_midia:
            return (False, "ID obrigatório para atualização completa.")
        conn = self.db.get_connection()
        if not conn:
            return (False, "Falha na conexão com o banco.")

        try:
            sql = """
                UPDATE tb_midia
                SET titulo = %s, tipo = %s, genero = %s, ano = %s, status = %s, nota = %s
                WHERE id_midia = %s
            """
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        midia.titulo.strip(),
                        midia.tipo,
                        midia.genero.strip() if midia.genero else None,
                        midia.ano,
                        midia.status,
                        midia.nota,
                        midia.id_midia,
                    ),
                )
                conn.commit()
                if cur.rowcount == 0:
                    return (False, "ID não encontrado.")
                return (True, "Registro atualizado!")
        except Error as e:
            if getattr(e, "errno", None) == 1062:
                return (False, "Conflito com título/ano/tipo já existente.")
            return (False, f"Erro ao atualizar: {e}")
        finally:
            self.db.close_connection(conn)

    # Função para excluir algum ítem do catálogo
    def delete(self, id_midia: int) -> tuple[bool, str]:
        conn = self.db.get_connection()
        if not conn:
            return (False, "Falha na conexão com o banco.")
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM tb_midia WHERE id_midia = %s", (int(id_midia),)
                )
                conn.commit()
                if cur.rowcount == 0:
                    return (False, "ID não encontrado.")
                return (True, "Excluído com sucesso!")
        except Error as e:
            return (False, f"Erro ao excluir: {e}")
        finally:
            self.db.close_connection(conn)

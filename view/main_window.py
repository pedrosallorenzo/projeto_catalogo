# Arquivo destinado à interface gráfica

import customtkinter as ctk
from tkinter import ttk, messagebox
from model.midia import Midia

TIPOS = ("Filme", "Serie")
STATUS = ("Pendente", "Assistido")


class CTKApp(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        self.title("Catálogo de Filmes & Séries")
        self.geometry("1260x640")
        self.controller = controller

        self._build()
        self._load_all()

    # Formulário

    def _build(self):
        frm = ctk.CTkFrame(self, corner_radius=10)
        frm.pack(fill="x", padx=10, pady=(10, 6))

        self.ent_titulo = ctk.CTkEntry(frm, placeholder_text="Título *", width=320)
        self.ent_titulo.grid(row=0, column=0, padx=6, pady=6, sticky="w")

        self.cmb_tipo = ctk.CTkOptionMenu(frm, values=list(TIPOS))
        self.cmb_tipo.set(TIPOS[0])
        self.cmb_tipo.grid(row=0, column=1, padx=6, pady=6)

        self.ent_genero = ctk.CTkEntry(frm, placeholder_text="Gênero")
        self.ent_genero.grid(row=0, column=2, padx=6, pady=6)

        self.ent_ano = ctk.CTkEntry(frm, placeholder_text="Ano", width=100)
        self.ent_ano.grid(row=0, column=3, padx=6, pady=6)

        self.cmb_status = ctk.CTkOptionMenu(frm, values=list(STATUS))
        self.cmb_status.set(STATUS[0])
        self.cmb_status.grid(row=0, column=4, padx=6, pady=6)

        self.ent_nota = ctk.CTkEntry(frm, placeholder_text="Nota (0–10)", width=120)
        self.ent_nota.grid(row=0, column=5, padx=6, pady=6)

        self.btn_add = ctk.CTkButton(frm, text="Adicionar", command=self._on_add)
        self.btn_add.grid(row=1, column=0, padx=6, pady=(0, 8), sticky="w")
        self.btn_upd = ctk.CTkButton(
            frm,
            text="Atualizar Selecionado",
            fg_color="#f59e0b",
            hover_color="#d97706",
            command=self._on_update,
        )
        self.btn_upd.grid(row=1, column=1, padx=6, pady=(0, 8))
        self.btn_del = ctk.CTkButton(
            frm,
            text="Excluir Selecionado",
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self._on_delete,
        )
        self.btn_del.grid(row=1, column=2, padx=6, pady=(0, 8))
        self.btn_clear = ctk.CTkButton(
            frm, text="Limpar Formulário", command=self._clear_form
        )
        self.btn_clear.grid(row=1, column=3, padx=6, pady=(0, 8))
        self.btn_reload = ctk.CTkButton(frm, text="Recarregar", command=self._load_all)
        self.btn_reload.grid(row=1, column=4, padx=6, pady=(0, 8))

        # Filtros
        f = ctk.CTkFrame(self, corner_radius=10)
        f.pack(fill="x", padx=10, pady=(0, 6))

        self.f_titulo = ctk.CTkEntry(f, placeholder_text="Título contém", width=220)
        self.f_titulo.grid(row=0, column=0, padx=6, pady=6)

        self.f_genero = ctk.CTkEntry(f, placeholder_text="Gênero", width=160)
        self.f_genero.grid(row=0, column=1, padx=6, pady=6)

        self.f_tipo = ctk.CTkOptionMenu(f, values=["", "Filme", "Serie"], width=120)
        self.f_tipo.set("")
        self.f_tipo.grid(row=0, column=2, padx=6, pady=6)

        self.f_status = ctk.CTkOptionMenu(f, values=[""] + list(STATUS))
        self.f_status.set("")
        self.f_status.grid(row=0, column=3, padx=6, pady=6)

        self.f_ano = ctk.CTkEntry(f, placeholder_text="Ano", width=80)
        self.f_ano.grid(row=0, column=4, padx=6, pady=6)

        self.f_nota_ordem = ctk.CTkOptionMenu(
            f, values=["", "Ascendente", "Descendente"], width=140
        )
        self.f_nota_ordem.set("")
        self.f_nota_ordem.grid(row=0, column=5, padx=6, pady=6)

        ctk.CTkButton(f, text="Aplicar Filtros", command=self._on_filter).grid(
            row=0, column=6, padx=6, pady=6
        )
        ctk.CTkButton(f, text="Limpar Filtros", command=self._clear_filters).grid(
            row=0, column=7, padx=6, pady=6
        )

        # Tabela
        wrap = ctk.CTkFrame(self, corner_radius=10)
        wrap.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        cols = ("id", "titulo", "tipo", "genero", "ano", "status", "nota")
        self.tv = ttk.Treeview(wrap, columns=cols, show="headings", height=14)
        for c, t in zip(
            cols, ("ID", "Título", "Tipo", "Gênero", "Ano", "Status", "Nota")
        ):
            self.tv.heading(c, text=t)
        self.tv.column("id", width=60, anchor="center")
        self.tv.pack(fill="both", expand=True, padx=4, pady=4)

        self.tv.bind("<<TreeviewSelect>>", self._on_select)

    # Ações
    def _load_all(self):
        self._clear_table()
        res = self.controller.listar_todas()
        if not res["ok"]:
            messagebox.showerror("Erro", res["msg"])
            return
        for m in res["data"]:
            self._insert(m)

    def _on_filter(self):
        ordem_lable = self.f_nota_ordem.get().strip().lower()
        nota_ordem = None

        if ordem_lable == "ascendente":
            nota_ordem = "asc"
        elif ordem_lable == "descendente":
            nota_ordem = "desc"

        res = self.controller.filtrar(
            titulo_like=self.f_titulo.get().strip(),
            genero=self.f_genero.get().strip(),
            status=self.f_status.get().strip(),
            tipo=self.f_tipo.get().strip(),
            ano=self.f_ano.get().strip(),
            nota_ordem=nota_ordem,
        )
        if not res["ok"]:
            messagebox.showwarning("Atenção", res["msg"])
            return
        self._clear_table()
        for m in res["data"]:
            self._insert(m)

    def _on_add(self):
        r = self.controller.adicionar(
            titulo=self.ent_titulo.get(),
            tipo=self.cmb_tipo.get(),
            genero=self.ent_genero.get(),
            ano=self.ent_ano.get(),
            status=self.cmb_status.get(),
            nota=self.ent_nota.get(),
        )
        messagebox.showinfo("Info", r["msg"] if r["ok"] else r["msg"])
        if r["ok"]:
            self._clear_form()
            self._load_all()

    def _on_update(self):
        it = self._sel()
        if not it:
            messagebox.showinfo("Info", "Selecione uma linha")
            return
        mid = int(it["values"][0])

        ano_int = self._parse_optional_int(self.ent_ano.get())
        nota_int = self._parse_optional_int(self.ent_nota.get())
        if ano_int == "__INVALID__":
            messagebox.showwarning("Atenção", "Ano inválido. Use apenas números.")
            return
        if nota_int == "__INVALID__":
            messagebox.showwarning(
                "Atenção",
                "Nota inválida. Use número inteiro entre 0 e 10 (ou deixe vazio).",
            )
            return
        if nota_int is not None and not (0 <= nota_int <= 10):
            messagebox.showwarning("Atenção", "Nota fora do intervalo 0–10.")
            return

        m = Midia(
            id_midia=mid,
            titulo=self.ent_titulo.get().strip(),
            tipo=self.cmb_tipo.get().strip().lower(),
            genero=(self.ent_genero.get().strip() or None),
            ano=ano_int,
            status=self.cmb_status.get().strip().lower(),
            nota=nota_int,
        )

        r = self.controller.atualizar_full(m)
        messagebox.showinfo("Info", r["msg"])
        if r["ok"]:
            self._load_all()

    def _on_delete(self):
        it = self._sel()
        if not it:
            messagebox.showinfo("Info", "Selecione uma linha")
            return
        mid = it["values"][0]
        if messagebox.askyesno("Confirmação", f"Excluir ID {mid}?"):
            r = self.controller.excluir(str(mid))
            messagebox.showinfo("Info", r["msg"])
            if r["ok"]:
                self._load_all()

    # Funções extras

    def _clear_form(self):
        for w in (self.ent_titulo, self.ent_genero, self.ent_ano, self.ent_nota):
            w.delete(0, "end")
        self.cmb_tipo.set(TIPOS[0])
        self.cmb_status.set(STATUS[0])

    def _clear_filters(self):
        self.f_titulo.delete(0, "end")
        self.f_genero.delete(0, "end")
        self.f_ano.delete(0, "end")
        self.f_nota_ordem.set("")
        self.f_tipo.set("")
        self.f_status.set("")

        self._load_all()

    def _clear_table(self):
        for i in self.tv.get_children():
            self.tv.delete(i)

    def _insert(self, m):
        self.tv.insert(
            "",
            "end",
            values=(
                m.id_midia,
                m.titulo,
                m.tipo.upper(),
                m.genero,
                m.ano,
                m.status.upper(),
                m.nota,
            ),
        )

    def _sel(self):
        s = self.tv.selection()
        return None if not s else self.tv.item(s[0])

    def _on_select(self, _):
        it = self._sel()
        if not it:
            return
        v = it["values"]
        self.ent_titulo.delete(0, "end")
        self.ent_titulo.insert(0, v[1] or "")
        self.cmb_tipo.set(str(v[2]).lower())
        self.ent_genero.delete(0, "end")
        if v[3]:
            self.ent_genero.insert(0, v[3])
        self.ent_ano.delete(0, "end")
        self.ent_ano.insert(0, "" if v[4] is None else v[4])
        self.cmb_status.set(str(v[5]).lower())
        self.ent_nota.delete(0, "end")
        if v[6] is not None:
            self.ent_nota.insert(0, v[6])

    def _parse_optional_int(self, txt: str):
        t = (txt or "").strip().lower()
        if t in ("", "none", "null", "-"):
            return None
        try:
            return int(t)
        except ValueError:
            return "__INVALID__"

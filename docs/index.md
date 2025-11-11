# Catálogo de Filmes & Séries

Aplicação CRUD simples para **cadastrar, consultar, atualizar e excluir** mídias (filmes e séries), com filtros por título, gênero, tipo, status, ano e **ordenação por nota (Crescente/Decrescente)**.

- **Stack**: Python 3.11+ · CustomTkinter (UI) · MySQL (local) · Padrão **MVC**
- **Objetivo acadêmico**: Atender aos requisitos do seminário de BD2 (CRUD + conexão a BD).

!!! tip "Resumo do CRUD"
    - **Create**: adiciona mídia com validações (tipo, status, nota 0–10).
    - **Read**: consulta e filtros combináveis; ordenação por nota oculta itens sem nota.
    - **Update**: atualização completa (título, tipo, gênero, ano, status, nota).
    - **Delete**: exclusão pelo ID.
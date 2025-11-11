# Estrutura e Arquitetura (MVC)

O projeto segue o padrão **MVC** (Model-View-Controller):


-   V[View (CustomTkinter)] -->|aciona| C[Controller]
-   C -->|envia dados| M[Model]
-   M -->|executa SQL| DB[(MySQL)]
-   DB --> M
-   M --> C
-   C --> V

## Pastas

- controller/  → Regras de negócio
- model/       → Conexão e comandos SQL
- view/        → Interface gráfica (CustomTkinter)
- database/    → Scripts e configuração
- main.py      → Ponto de entrada
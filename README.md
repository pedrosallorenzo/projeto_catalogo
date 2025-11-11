# 🎬 Catálogo de Filmes & Séries

Aplicação desktop desenvolvida em **Python + MySQL**, com interface moderna feita em **CustomTkinter** e arquitetura **MVC** (Model–View–Controller).  
Permite cadastrar, consultar, atualizar e excluir filmes e séries, além de aplicar filtros e ordenar resultados por nota.

🔗 **Documentação completa:** [https://pedrosallorenzo.github.io/projeto_catalogo](https://pedrosallorenzo.github.io/projeto_catalogo)

---

## 🚀 Funcionalidades principais

- **CREATE:** cadastro de filmes e séries com validação dos campos.  
- **READ:** listagem com filtros por título, tipo, gênero, status e ano.  
- **UPDATE:** atualização do registro selecionado.  
- **DELETE:** exclusão direta da tabela.  
- **FILTROS AVANÇADOS:**
  - Ordenação por **nota Crescente/Decrescente** (oculta itens sem nota).
  - Filtragem combinada (ex.: tipo + status + ano).

---

## 🧱 Arquitetura (MVC)

├── config/       # Conexão com o banco de dados (MySQL)
├── controller/   # Regras de negócio e ligação entre View e Model
├── model/        # Lógica de acesso e manipulação do banco
├── view/         # Interface gráfica (CustomTkinter)
├── tests/        # Scripts e testes manuais
├── main.py       # Ponto de entrada da aplicação
└── requirements.txt

---

## 🧱 Arquitetura (MVC)

Banco MySQL local com tabela única:

CREATE TABLE tb_midia (
  id_midia INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(100) NOT NULL,
  tipo ENUM('FILME','SERIE') NOT NULL,
  genero VARCHAR(50),
  ano INT,
  status ENUM('PENDENTE','ASSISTIDO'),
  nota INT CHECK (nota BETWEEN 0 AND 10)
);

---

## Como executar

**1. Clonar o repositório**
git clone https://github.com/pedrosallorenzo/projeto_catalogo.git
cd projeto_catalogo

**2️. Criar o ambiente virtual**
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

**3. Rodar o sistema**
python main.py

---

## Padrão adotado

O projeto segue o padrão MVC, separando:

- **Model:** regras de acesso ao banco e validações.

- **View:** interface (CustomTkinter).

- **Controller:** controle da lógica de CRUD e comunicação entre camadas.

---

## Testes manuais
Ação        ->	    Resultado esperado
Adicionar   ->      Filme	Novo item aparece na lista
Atualizar   ->      Dados atualizados com sucesso
Excluir     ->	    Item removido
Filtrar     ->      “Filme”	Exibe apenas filmes
Ordenar     ->      “Decrescente”	Exibe itens com nota do maior ao menor

---

## Tecnologias utilizadas

- Categoria	Ferramenta
- Linguagem	Python 3.11+
- Banco de dados	MySQL
- Interface	CustomTkinter
- Padrão	MVC
- Documentação	MkDocs + Material Theme

---

## Documentação online

Acesse a documentação completa do projeto (gerada com MkDocs Material) clicando no link abaixo:
**https://pedrosallorenzo.github.io/projeto_catalogo/**

---

## Licença

Este projeto foi desenvolvido para fins educacionais e pode ser reutilizado livremente com atribuição de crédito.

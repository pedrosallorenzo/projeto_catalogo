# Instalação e Requisitos

## Requisitos mínimos
- Python 3.11 ou superior  
- MySQL instalado localmente (porta padrão 3306)

## Passos para configurar

- git clone https://github.com/SEU_USUARIO/projeto_catalogo.git
- cd projeto_catalogo
- python -m venv .venv
- .venv\Scripts\activate
- pip install -r requirements.txt

## Crie o banco de dados no MySQL WorkBench 8.0 CE

- CREATE DATABASE db_projeto_catalogo;

- USE db_projeto_catalogo;

- CREATE TABLE IF NOT EXISTS tb_midia (
   id_midia INT AUTO_INCREMENT PRIMARY KEY,
   titulo   VARCHAR(100) NOT NULL,
   tipo     ENUM('FILME','SERIE') NOT NULL,
   genero   VARCHAR(60) NULL,
   ano      INT NULL,
   status   ENUM('PENDENTE','ASSISTIDO') NOT NULL DEFAULT 'PENDENTE',
   nota     INT NULL,
   CONSTRAINT chk_nota CHECK (nota IS NULL OR (nota BETWEEN 0 AND 10))
 );

## Crie um arquivo .env para colocar informações pessoais do banco de dados local

- DB_HOST=127.0.0.1
- DB_PORT=3306
- DB_USER=root
- DB_PASSWORD=<sua_senha>
- DB_NAME=db_projeto_catalogo


## `docs/running.md`
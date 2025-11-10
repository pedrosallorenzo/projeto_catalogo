-- Banco de dados Projeto Catálogo (BD2)

-- Criar e usar
create database db_projeto_catalogo;
use db_projeto_catalogo;

create table tb_midia
(id_midia int not null auto_increment primary key,
titulo varchar(120) not null,
tipo enum('FILME', 'SERIE') not null,
genero varchar(40) null,
ano int null,
status enum('pendente', 'assistido') not null default 'pendente',
nota int null,
created_at timestamp not null default current_timestamp,
unique key uk_midia (titulo, ano, tipo),
key idx_titulo (titulo),
key idx_genero (genero),
key idx_status (status),
key idx_ano (ano));

alter table tb_midia
add constraint chk_nota_valida check (nota is null or (nota between 0 and 10));


-- Dados para testes
insert into tb_midia
(titulo, tipo, genero, ano, status, nota)
values
('Matrix',              'filme', 'Ficção',   1999, 'assistido', 10),
('Oppenheimer',         'filme', 'Drama',    2023, 'pendente',  NULL),
('The Last of Us',      'serie', 'Drama',    2023, 'assistido', 9),
('Breaking Bad',        'serie', 'Crime',    2008, 'pendente',  NULL),
('Inception',           'filme', 'Ação',     2010, 'assistido', 9),
('Duna: Parte Dois',    'filme', 'Ficção',   2024, 'pendente',  NULL);

select * from tb_midia;


-- OBS.: O banco de dados vai rodar localmente!
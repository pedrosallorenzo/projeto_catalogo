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


-- Dados para popular o sistema
insert into tb_midia
(titulo, tipo, genero, ano, status, nota)
values
('Matrix',                   'filme', 'Ficção',      1999, 'assistido', 10),
('Oppenheimer',              'filme', 'Drama',       2023, 'pendente',  NULL),
('The Last of Us',           'serie', 'Drama',       2023, 'assistido', 9),
('Breaking Bad',             'serie', 'Crime',       2008, 'pendente',  NULL),
('Inception',                'filme', 'Ação',        2010, 'assistido', 9),
('Duna: Parte Dois',         'filme', 'Ficção',      2024, 'pendente',  NULL),
('Interstellar',             'filme', 'Ficção',      2014, 'assistido', 10),
('Parasita',                 'filme', 'Drama',       2019, 'assistido', 9),
('Stranger Things',          'serie', 'Ficção',      2016, 'assistido', 8),
('The Batman',               'filme', 'Ação',        2022, 'pendente',  NULL),
('O Senhor dos Anéis',       'filme', 'Fantasia',    2001, 'assistido', 10),
('Game of Thrones',          'serie', 'Fantasia',    2011, 'assistido', 8),
('Avatar: O Caminho da Água','filme', 'Ficção',      2022, 'pendente',  NULL),
('The Boys',                 'serie', 'Ação',        2019, 'assistido', 9),
('Chernobyl',                'serie', 'Drama',       2019, 'assistido', 10),
('O Poderoso Chefão',        'filme', 'Crime',       1972, 'assistido', 10),
('Peaky Blinders',           'serie', 'Crime',       2013, 'assistido', 9),
('Gladiador',                'filme', 'Ação',        2000, 'assistido', 9),
('O Lobo de Wall Street',    'filme', 'Drama',       2013, 'assistido', 8),
('House of the Dragon',      'serie', 'Fantasia',    2022, 'pendente',  NULL),
('Black Mirror',             'serie', 'Ficção',      2011, 'assistido', 8),
('O Clube da Luta',          'filme', 'Drama',       1999, 'assistido', 9),
('Vingadores: Ultimato',     'filme', 'Ação',        2019, 'assistido', 9),
('Rick and Morty',           'serie', 'Animação',    2013, 'assistido', 8),
('The Mandalorian',          'serie', 'Ficção',      2019, 'pendente',  NULL),
('Joker',                    'filme', 'Drama',       2019, 'assistido', 9),
('Narcos',                   'serie', 'Crime',       2015, 'assistido', 8),
('Tenet',                    'filme', 'Ação',        2020, 'pendente',  NULL),
('Shrek',                    'filme', 'Animação',    2001, 'assistido', 8),
('The Witcher',              'serie', 'Fantasia',    2019, 'pendente',  NULL);

select * from tb_midia;

alter table tb_midia
auto_increment = 7;


-- OBS.: O banco de dados vai rodar localmente!
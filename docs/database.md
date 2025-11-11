# Banco de Dados

O sistema utiliza um único banco (`db_catalogo`) com uma tabela central `tb_midia`.

### Estrutura
| Campo | Tipo | Descrição |
|--------|------|-----------|
| id_midia | INT | Identificador único (PK) |
| titulo | VARCHAR(100) | Nome do filme/série |
| tipo | ENUM | FILME ou SERIE |
| genero | VARCHAR(50) | Categoria |
| ano | INT | Ano de lançamento |
| status | ENUM | PENDENTE ou ASSISTIDO |
| nota | INT | Avaliação de 0 a 10 |

IDs não são reordenados após exclusão (decisão de integridade).
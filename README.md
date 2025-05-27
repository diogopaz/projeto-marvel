#  Análise de Dados da Marvel API com Python

Este projeto consome dados da [Marvel Comics API](https://developer.marvel.com/) e realiza análises exploratórias para descobrir insights sobre personagens, quadrinhos, eventos e séries.

A aplicação foi desenvolvida em **Python** com uso de bibliotecas como `pandas`, `numpy`, `matplotlib`, etc... e executada em um ambiente do **Google Colab**.
Nesta branch está disponível o script (`main.py`), que corresponde ao Backend do projeto. Para rodar o código de forma interativa pelo **Google Colab**, por favor acesse a branch `colab`.

---

# Backend ETL da Marvel API

Este script Python (`main.py`) é responsável por coletar, tratar e armazenar dados da Marvel API em um banco de dados SQLite. Ele atua como backend do projeto, realizando o processo de ETL (Extract, Transform, Load), deixando os dados prontos para serem utilizados em análises, visualizações ou outras formas de apresentação.

## Funcionalidades

- Extrai dados da API da Marvel (personagens, quadrinhos, criadores)
- Trata os dados, estruturando informações como:
  - Relação de quadrinhos por personagem
  - Preços e criadores associados a quadrinhos
- Armazena os dados em um banco de dados SQLite local
- Exporta também os dados brutos em formato `.csv`

---

## Como executar

Você pode executar o script diretamente pela linha de comando, usando Python 3:

```bash
python main.py [opções]
```

### Parâmetros disponíveis

| Parâmetro        | Ação                                                         |
| ---------------- | ------------------------------------------------------------ |
| `--characters`   | Executa apenas o ETL de personagens                          |
| `--comics`       | Executa apenas o ETL de quadrinhos                           |
| `--creators`     | Executa apenas o ETL de criadores                            |
| `--all`          | Executa o ETL completo (personagens, quadrinhos e criadores) |
| `--db-name NOME` | Define o nome do arquivo `.db` (padrão: `marvel.db`)         |

> Se nenhuma opção for passada, o script executa o ETL completo por padrão (equivalente a `--all`).

### Exemplos de uso

Executar o ETL completo:

```bash
python main.py
```

Executar apenas os personagens e salvar em `dados.db`:

```bash
python main.py --characters --db-name dados
```

Executar quadrinhos e criadores:

```bash
python main.py --comics --creators
```

---

## Configuração das chaves da API

Você precisa de uma conta na [Marvel Developer Portal](https://developer.marvel.com) para obter suas chaves.

Crie um arquivo chamado `.env` no mesmo diretório do script com o seguinte conteúdo:

```
MARVEL_PUBLIC_KEY=sua_chave_publica
MARVEL_PRIVATE_KEY=sua_chave_privada
```

---

## Estrutura das tabelas geradas

O banco SQLite conterá tabelas como:

- `characters`: ID, nome, descrição, data de modificação e número de quadrinhos
- `character_comics`: relação entre personagens e quadrinhos
- `comics`: ID, título, número de páginas e variantes
- `comic_prices`: preços dos quadrinhos (digital, print, etc.)
- `comic_creators`: relação entre quadrinhos e criadores, com os respectivos papéis
- `creators`: informações sobre os criadores (nome completo, sufixos, etc.)

---

## Próximos passos

Com os dados organizados e salvos, você pode utilizar bibliotecas como **Pandas**, **Plotly**, **Matplotlib** ou frameworks web para gerar dashboards, gráficos interativos e análises com base nas informações coletadas.

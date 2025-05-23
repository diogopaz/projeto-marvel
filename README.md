#  Análise de Dados da Marvel API com Python

Este projeto consome dados da [Marvel Comics API](https://developer.marvel.com/) e realiza análises exploratórias para descobrir insights sobre personagens, quadrinhos, eventos e séries.

A aplicação foi desenvolvida em **Python** com uso de bibliotecas como `pandas`, `numpy`, `matplotlib`, etc... e executada em um ambiente do **Google Colab**.

---

##  Objetivo

- Explorar os dados públicos da Marvel de forma interativa.
- Aplicar boas práticas de desenvolvimento no processo.
- Encontrar insights significativos no meio da vasta gama de informação presente na API.

---

##  Tecnologias Utilizadas

- Python 3
- Google Colab
- [Marvel API](https://developer.marvel.com/)
- `hashlib`
- `plotly`
- `pandas`
- `numpy`
- `matplotlib`
- `dotenv`
- `sqlite3` (opcional, para persistência local de dados)


---

##  How To:
Ao longo do arquivo estão presentes campos de texto `Markdown` que explicam como utilizar cada parte do arquivo

## Novas análises sem uma API key:
Para evitar atrasos na realização de novas análises em cima dos dados extraídos da API, disponibilizamos o arquivo compactado [BD_21-05-25.7z](BD_21-05-25.7z), que conta com os dados brutos extraídos de cada endpoint em arquivos `.csv`  e o banco com os dados mais atualizados da API até a data descrita no título do arquivo. Dessa forma, é possível visualizar os insights obtidos sem a necessidade de realizar novas requisições, basta fazer upload do arquivo `marvel.db` no ambiente de execução do Colab e rodar as células da seção `Insights`. Isso também descarta a necessidade de criar uma conta para obter uma chave para requisições da API.


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
Ao longo do arquivo [`projeto_marvel.pynb`](projeto_marvel.ipynb) estão presentes campos de texto `Markdown` com instruções de como executar cada parte do código.

### Passo 1: Obtenha as Chaves da Marvel
A API da marvel exige uma chave pública e uma privada para realizar requisições.

Crie uma conta gratuita em https://developer.marvel.com/ e pegue suas chaves que serão utilizadas no código como:

- `MARVEL_PUBLIC_KEY`
- `MARVEL_PRIVATE_KEY`

Existem duas formas de utilizar as suas chaves para realizar requisições executando o código, usando `<i/>Secrets</i>` do próprio <i/>Google Colab</i> ou com um arquivo `.env`.

Ambos métodos estão descritos no notebook com o código fonte do projeto.

### Passo 2: Abrir o arquivo no Google Colab
No início do arquivo [`projeto_marvel.pynb`](projeto_marvel.ipynb) existe um botão `Open in Colab` com o link para abrí-lo direto no Colab.

### Passo 3: Executar as células de código na ordem.
Para realizar o fluxo principal de execução (Obter os dados da API, tratá-los, salvar no banco de dados e, por fim, realizar análises a partir desses dados), basta executar as células na ordem em que aparecem no `.ipynb`.

## Novas análises sem uma API key:
Para evitar atrasos na realização de novas análises em cima dos dados extraídos da API, disponibilizamos o arquivo compactado [BD_21-05-25.7z](BD_21-05-25.7z), que conta com os dados brutos extraídos de cada endpoint em arquivos `.csv`  e o banco com os dados mais atualizados da API até a data descrita no título do arquivo.

Após fazer upload do banco de dados `marvel.db` no ambiente de execução do Google Colab, é possível visualizar os insights obtidos sem a necessidade de realizar novas requisições, basta rodar as células da seção `Insights`. Isso também descarta a necessidade de criar uma conta para obter uma chave para requisições da API.


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

##  Como Usar com Segurança (Google Colab)

### Passo 1: Obtenha as Chaves da Marvel

Crie uma conta gratuita em https://developer.marvel.com/ e pegue sua:

- `MARVEL_PUBLIC_KEY`
- `MARVEL_PRIVATE_KEY`

### Passo 2: crie um arquivo chamado .env.

##### o .env é um arquivo que é visivel para o OS.

```python
MARVEL_PUBLIC_KEY = public_key
MARVEL_PRIVATE_KEY = private_key
```

Realize as alterações a fim de se ajustar a sua conta Marvel.

### Passo 3: Executar as células de código na ordem.

#### 3.1 install dotenv.

```python
!pip install dotenv
```
A linha acima estará comentada para dar inicio a instalação do `dotenv` é necessário remover o `#` e executar a célula.

#### 3.2 imports de bibliotecas.
```python
import requests
import hashlib
import time
import os
import pandas as pd
from dotenv import load_dotenv
import sqlite3
from google.colab import userdata
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
```
após isso executar a célula resposável por importar as bibliotecas.

#### 3.3 Carregar variaveis de ambiente.
```python
load_dotenv(dotenv_path='/content/.env')
public_key = os.getenv('MARVEL_PUBLIC_KEY')
private_key = os.getenv('MARVEL_PRIVATE_KEY')
```
Essa célula é resposável por carregar as variáveis de ambiente ou seja as senhas do `.env`.

#### 3.4 Montando os parâmetros para realizar a requisição.

```python
ts = str(time.time())
to_hash = ts + str(private_key) + str(public_key)
hash_md5 = hashlib.md5(to_hash.encode('utf-8')).hexdigest()

params = {
    'apikey': public_key,
    'ts': ts,
    'hash': hash_md5,
    'limit': 10
}
```


#### 3.5 Criação de tabelas no sqlite.

```python
url = 'https://gateway.marvel.com/v1/public/characters'

response = requests.get(url, params=params)
data = response.json()
```



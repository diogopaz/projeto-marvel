import requests
import hashlib
import time
import os
import pandas as pd
from dotenv import load_dotenv
import sqlite3

load_dotenv(dotenv_path='/.env')
public_key = os.getenv('MARVEL_PUBLIC_KEY')
private_key = os.getenv('MARVEL_PRIVATE_KEY')

def get_auth_params():
    ts = str(time.time())
    to_hash = ts + private_key + public_key
    hash_md5 = hashlib.md5(to_hash.encode()).hexdigest()
    return {
        'ts': ts,
        'apikey': public_key,
        'hash': hash_md5
    }

def fetch_from_marvel(endpoint, limit = 100, offset = 0):
  "Busca todos os resultados de um endpoint paginado da Marvel API"
  limit = limit
  offset = offset
  all_results = []
  total = 1
  req_count = 0

  print(f"Iniciando requisições para o endpoint: {endpoint}")

  while offset < total:
    params = get_auth_params()
    params["limit"] = limit
    params["offset"] = offset

    try:
      response = requests.get(endpoint, params=params)
      response.raise_for_status()
      data = response.json().get("data", {})
      total = data['total']
      results = data.get("results", [])
      if not results:
        break

      all_results.extend(results)
      print(f"Recebidos {len(results)} resultados (offset {offset})")

      offset += limit
      req_count += 1
      time.sleep(1)
    except Exception as e:
      print(f"Erro em offset {offset}: {e}. Pulando...")
      offset += limit
      req_count += 1
      time.sleep(1)

  # Exportando dados brutos para csv
  df = pd.DataFrame(all_results)
  df.to_csv(f'{endpoint.split("/")[-1]}.csv')

  print(f'''
  Sucesso! Recebidos {len(all_results)} resultados.
  Requisições realizadas: {req_count}.
  Dados brutos salvos em: {endpoint.split("/")[-1]}.csv
  ''')

  return df

def to_db(df, table_name, db_name):
  try:
    conn = sqlite3.connect(f"{db_name}.db")
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    conn.commit()
    conn.close()
    print('Dados salvos no banco')
  except Exception as e:
    conn.close()
    print(e)

def extract_comic_prices(df_comics):
  records = []
  for _, row in df_comics.iterrows():
    comic_id = row.get('id')
    for price in row.get('prices', []):
      records.append({
        'comic_id': comic_id,
        'type': price.get('type', ''),
        'price': price.get('price', 0.0)
      })
  return pd.DataFrame(records)


def extract_comic_creators(df_comics):
  records = []
  for _, row in df_comics.iterrows():
    comic_id = row.get('id')
    for creator in row.get('creators', {}).get('items', []):
      try:
        resource_uri = creator.get('resourceURI', '')
        creator_id = int(resource_uri.strip().split('/')[-1])
        role = creator.get('role', '')
        records.append({
          'comic_id': comic_id,
          'creator_id': creator_id,
          'role': role
        })
      except (IndexError, ValueError):
        continue
  return pd.DataFrame(records)

def extract_character_comics(character_ids):
    all_pairs = []

    for character_id in character_ids:
        print(f"Buscando comics para o personagem {character_id}...")
        try:
            endpoint = f"https://gateway.marvel.com/v1/public/characters/{character_id}/comics"
            limit = 100
            offset = 0
            total = 1

            while offset < total:
                params = get_auth_params()
                params.update({"limit": limit, "offset": offset})
                response = requests.get(endpoint, params=params)
                response.raise_for_status()
                data = response.json().get("data", {})
                total = data.get("total", 0)
                results = data.get("results", [])

                for comic in results:
                    comic_id = comic.get("id")
                    if comic_id:
                        all_pairs.append({
                            "character_id": character_id,
                            "comic_id": comic_id
                        })

                offset += limit
                time.sleep(0.1)

        except Exception as e:
            print(f"Erro ao processar o personagem {character_id}: {e}")

    df = pd.DataFrame(all_pairs)
    return df

characters = fetch_from_marvel('https://gateway.marvel.com/v1/public/characters')
characters['comics_available'] = characters['comics'].apply(lambda x: x.get('available'))
characters = characters[['id', 'name', 'description', 'modified', 'comics_available']]

# Para nossa análise, precisamos armazenar a relação personagem/quadrinho apenas dos 10 personagens que mais possuem quadrinhos
top_10_ids = characters.sort_values(by="comics_available", ascending=False).head(10)["id"].tolist()
character_comics = extract_character_comics(top_10_ids)

# Salvando o personagens e a relação personagem/quadrinho no banco
to_db(characters, table_name='characters', db_name='marvel')
to_db(character_comics, table_name='character_comics', db_name='marvel')

comics = fetch_from_marvel('https://gateway.marvel.com/v1/public/comics')
comic_prices = extract_comic_prices(comics)
comic_creators = extract_comic_creators(comics)

comics['variant_count'] = comics['variants'].apply(lambda x: len(x))
comics['page_count'] = comics['pageCount']
comics = comics[['id', 'title', 'page_count', 'variant_count']]

# Salvando os dados de quadrinhos e as relações quadrinho/preços e quadrinho/criadores no banco:
to_db(comics, table_name='comics', db_name='marvel')
to_db(comic_prices, table_name='comic_prices', db_name='marvel')
to_db(comic_creators, table_name='comic_creators', db_name='marvel')

creators = fetch_from_marvel('https://gateway.marvel.com/v1/public/creators', 20)
# Pegando 20 resultados por requisição, pois este endpoint possui muitos offsets que retornam erro

creators = creators[['id', 'firstName', 'middleName', 'lastName', 'suffix', 'fullName', 'modified']]
to_db(creators, table_name='creators', db_name='marvel')
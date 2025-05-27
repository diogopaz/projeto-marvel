import requests
import hashlib
import time
import os
import pandas as pd
from dotenv import load_dotenv
import sqlite3
import argparse

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

# Função principal de requisições
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

    df = pd.DataFrame(all_results)
    df.to_csv(f'{endpoint.split("/")[-1]}.csv')

    print(f'''
Sucesso! Recebidos {len(all_results)} resultados.
Requisições realizadas: {req_count}.
Dados brutos salvos em: {endpoint.split("/")[-1]}.csv
''')
    return df

# Salva no banco de dados
def to_db(df, table_name, db_name):
    if df.empty:
        print(f"DataFrame para '{table_name}' está vazio. Nada a salvar no banco '{db_name}'.")
        return
    try:
        conn = sqlite3.connect(f"{db_name}.db")
        df.to_sql(table_name, conn, index=False, if_exists='replace')
        conn.commit()
        conn.close()
        print('Dados salvos no banco')
    except Exception as e:
        print(e)

# Extrai os preços disponíveis para cada quadrinho
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

# Extrai os criadores de cada quadrinho
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

# Extrai os quadrinhos em que cada personagem está presente
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

# Funções para encapsular cada etapa do ETL
def run_characters_etl(db_name_param='marvel'):
    print("\n--- EXECUTANDO ETL DE PERSONAGENS ---")
    characters = fetch_from_marvel('https://gateway.marvel.com/v1/public/characters')
    if not characters.empty:
        characters['comics_available'] = characters['comics'].apply(lambda x: x.get('available') if isinstance(x, dict) else 0)
        characters = characters[['id', 'name', 'description', 'modified', 'comics_available']]
        top_10_ids = characters.sort_values(by="comics_available", ascending=False).head(10)["id"].tolist()
        character_comics = extract_character_comics(top_10_ids)
        to_db(characters, table_name='characters', db_name=db_name_param)
        to_db(character_comics, table_name='character_comics', db_name=db_name_param)
    else:
        print("Nenhum dado de personagem retornado pela API.")
    print("--- ETL DE PERSONAGENS CONCLUÍDO ---")

def run_comics_etl(db_name_param='marvel'):
    print("\n--- EXECUTANDO ETL DE QUADRINHOS ---")
    comics = fetch_from_marvel('https://gateway.marvel.com/v1/public/comics')
    if not comics.empty:
        comic_prices = extract_comic_prices(comics)
        comic_creators = extract_comic_creators(comics)
        comics['variant_count'] = comics['variants'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        comics['page_count'] = comics['pageCount']
        comics = comics[['id', 'title', 'page_count', 'variant_count']]
        to_db(comics, table_name='comics', db_name=db_name_param)
        to_db(comic_prices, table_name='comic_prices', db_name=db_name_param)
        to_db(comic_creators, table_name='comic_creators', db_name=db_name_param)
    else:
        print("Nenhum dado de quadrinhos retornado pela API.")
    print("--- ETL DE QUADRINHOS CONCLUÍDO ---")

def run_creators_etl(db_name_param='marvel'):
    print("\n--- EXECUTANDO ETL DE CRIADORES ---")
    creators = fetch_from_marvel('https://gateway.marvel.com/v1/public/creators', 20)
    if not creators.empty:
        creators = creators[['id', 'firstName', 'middleName', 'lastName', 'suffix', 'fullName', 'modified']]
        to_db(creators, table_name='creators', db_name=db_name_param)
    else:
        print("Nenhum dado de criador retornado pela API.")
    print("--- ETL DE CRIADORES CONCLUÍDO ---")

# Implementando argumentos
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ferramenta ETL para a API da Marvel.")
    parser.add_argument("--characters", action="store_true", help="Executar ETL apenas para Personagens.")
    parser.add_argument("--comics", action="store_true", help="Executar ETL apenas para Quadrinhos.")
    parser.add_argument("--creators", action="store_true", help="Executar ETL apenas para Criadores.")
    parser.add_argument("--all", action="store_true", help="Executar ETL para todos os tipos de dados.")
    parser.add_argument("--db-name", type=str, default="marvel", help="Nome base para o arquivo do banco de dados (ex: marvel gerará marvel.db).")

    args = parser.parse_args()

    db_to_use = args.db_name

    # Executa todas as etapas se não for passado nenhum argumento
    run_everything = not (args.characters or args.comics or args.creators) or args.all

    if args.characters or run_everything:
        run_characters_etl(db_name_param=db_to_use)

    if args.comics or run_everything:
        run_comics_etl(db_name_param=db_to_use)

    if args.creators or run_everything:
        run_creators_etl(db_name_param=db_to_use)

    if not (args.characters or args.comics or args.creators or run_everything):
        print("Nenhuma tarefa específica foi selecionada. Use --help para ver as opções.")
        parser.print_help()
    else:
        print("\nProcesso ETL finalizado.")

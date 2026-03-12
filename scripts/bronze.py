import requests
import json
import os

def fetch_api_data(max_pages=50):
    base_url = "https://api.openbrewerydb.org/v1/breweries" # [cite: 5]
    all_data = []
    
    # Paginação segura: evita loop infinito e trata erros de rede 
    for page in range(1, max_pages + 1):
        try:
            response = requests.get(base_url, params={"page": page, "per_page": 50}, timeout=15)
            response.raise_for_status()
            data = response.json()
            if not data: break
            all_data.extend(data)
        except Exception as e:
            print(f"Erro na extração: {e}")
            break

    os.makedirs('data/bronze', exist_ok=True)
    path = 'data/bronze/raw_breweries.json'
    with open(path, 'w') as f:
        json.dump(all_data, f)
    return path
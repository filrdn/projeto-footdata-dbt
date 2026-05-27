import os
import json
import requests

# 1. Configurações de Autenticação e Endpoint

API_KEY = '6b36949a907efaa3385fdaeed2a03534'
URL = "https://v3.football.api-sports.io/fixtures"

headers = {
    'x-apisports-key': API_KEY
}

# Filtro para trazer o Brasileirão
querystring = {"league": "71", "season": "2023"}

print("Iniciando a requisição para a API-Football baseado na documentação...")

try:
    # 2. Fazendo a busca dos dados
    response = requests.get(URL, headers=headers, params=querystring)
    response.raise_for_status() 
    
    data = response.json()
    
    if data.get("errors"):
        print(f"❌ Erro retornado pela API: {data['errors']}")
    else:
        # 3. Caminho da pasta Bronze
        output_dir = os.path.join('..', 'data', 'bronze')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'brasileirao_2023_raw.json')
        
        # 4. Salvando o arquivo
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Sucesso total! Dados salvos em: {output_path}")
        print(f"Total de partidas coletadas: {len(data.get('response', []))}")

except requests.exceptions.RequestException as e:
    print(f"❌ Erro de conexão ao tentar acessar a API: {e}")
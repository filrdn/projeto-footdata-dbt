import os
import json
import psycopg2

# 1. Configurações de Conexão com o Banco de Dados (PostgreSQL)
DB_CONFIG = {
    "dbname": "footdata_dw",
    "user": "postgres",
    "password": "bobesponja",
    "host": "localhost",
    "port": "5432"
}

# 2. Definindo o caminho do arquivo JSON que criamos no passo anterior
json_path = os.path.join('..', 'data', 'bronze', 'brasileirao_2023_raw.json')

print("Iniciando o processo de carga na camada Bronze do DW...")

# Valida se o arquivo JSON realmente existe na pasta antes de tentar abrir
if not os.path.exists(json_path):
    # Se você salvou com o ano de 2023 no nome do arquivo, vamos tentar ler o de 2023
    json_path = os.path.join('..', 'data', 'bronze', 'brasileirao_2023_raw.json')

try:
    # 3. Lendo os dados do arquivo JSON local
    with open(json_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
        
    partidas = payload.get("response", [])
    print(f"Arquivo carregado da memória. Encontradas {len(partidas)} partidas para inserir.")

    # 4. Conectando no banco de dados usando o psycopg2
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 5. Criando a tabela Bronze caso ela não exista
    # Armazenamos a estrutura inteira da partida como um tipo JSONB (JSON binário do Postgres)
    # Isso é uma prática padrão de mercado para tabelas Raw/Bronze!
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.brasileirao_fixtures_bronze (
            id_partida INT PRIMARY KEY,
            dados_brutos JSONB,
            carregado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # 6. Fazendo a carga dos dados (Loop inserindo linha por linha)
    for partida in partidas:
        id_partida = partida.get("fixture", {}).get("id")
        dados_brutos = json.dumps(partida)
        
        # O comando ON CONFLICT garante a IDEMPOTÊNCIA (se rodar 2 vezes, ele atualiza em vez de duplicar)
        cursor.execute("""
            INSERT INTO public.brasileirao_fixtures_bronze (id_partida, dados_brutos)
            VALUES (%s, %s)
            ON CONFLICT (id_partida) DO UPDATE 
            SET dados_brutos = EXCLUDED.dados_brutos;
        """, (id_partida, dados_brutos))

    # Salva as alterações de verdade no banco de dados (Commit)
    conn.commit()
    print("✅ Carga executada com sucesso! Dados inseridos na tabela public.brasileirao_fixtures_bronze")

except Exception as e:
    print(f"❌ Erro crítico durante o processo de carga: {e}")
    if 'conn' in locals():
        conn.rollback() # Cancela as operações se deu erro no meio do caminho

finally:
    # Garante que as conexões com o banco sejam fechadas para não gastar memória
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
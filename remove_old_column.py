import os
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# SQL para remover a coluna antiga
sql = '''
-- Remover a coluna muscle_group_id da tabela exercises
alter table exercises drop column if exists muscle_group_id;
'''

payload = {
    "sql": sql
}

response = requests.post(
    f"{SUPABASE_URL}/rest/v1/rpc/execute_sql",
    headers=headers,
    json=payload
)

if response.status_code == 200:
    print("Coluna muscle_group_id removida com sucesso da tabela exercises!")
else:
    print("Erro ao remover coluna:", response.text)
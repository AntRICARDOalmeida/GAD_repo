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

# SQL para migrar para o novo modelo many-to-many
sql = '''
-- 1. Criar nova tabela para relação many-to-many
create table if not exists exercise_muscle_groups (
    id serial primary key,
    exercise_id integer references exercises(id) on delete cascade,
    muscle_group_id integer references muscle_groups(id) on delete cascade,
    unique(exercise_id, muscle_group_id)
);

-- 2. Migrar dados existentes da tabela exercises para exercise_muscle_groups
insert into exercise_muscle_groups (exercise_id, muscle_group_id)
select id, muscle_group_id 
from exercises 
where muscle_group_id is not null
on conflict (exercise_id, muscle_group_id) do nothing;

-- 3. Remover a coluna muscle_group_id da tabela exercises (será feito depois de verificar que tudo funciona)
-- alter table exercises drop column if exists muscle_group_id;
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
    print("Migração executada com sucesso!")
    print("A coluna muscle_group_id ainda existe na tabela exercises para compatibilidade.")
    print("Execute o script remove_old_column.py depois de verificar que tudo funciona.")
else:
    print("Erro na migração:", response.text)
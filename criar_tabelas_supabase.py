import os
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Endpoint SQL do Supabase
sql_url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# SQL para criar todas as tabelas do modelo de dados
sql = '''
create table if not exists muscle_groups (
    id serial primary key,
    name text unique not null
);

create table if not exists exercises (
    id serial primary key,
    name text unique not null,
    muscle_group_id integer references muscle_groups(id)
);

create table if not exists sessions (
    id serial primary key,
    session_date timestamp not null,
    created_at timestamp default now()
);

create table if not exists session_exercises (
    id serial primary key,
    session_id integer references sessions(id),
    exercise_id integer references exercises(id)
);

create table if not exists sets (
    id serial primary key,
    session_exercise_id integer references session_exercises(id),
    set_number integer not null,
    weight float not null,
    reps integer,
    created_at timestamp default now()
);
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
    print("Tabelas criadas com sucesso!")
else:
    print("Erro ao criar tabelas:", response.text)

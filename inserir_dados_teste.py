from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inserir grupos musculares
muscle_groups = [
    {"name": "Peito"},
    {"name": "Costas"},
    {"name": "Pernas"},
    {"name": "Ombros"},
    {"name": "Bíceps"},
    {"name": "Tríceps"}
]
resp = supabase.table("muscle_groups").insert(muscle_groups).execute()
print("Muscle groups:", resp.data)

# Inserir exercícios
# Assumindo que os IDs dos grupos musculares são 1 a 6
exercises = [
    {"name": "Supino reto", "muscle_group_id": 1},
    {"name": "Remada curvada", "muscle_group_id": 2},
    {"name": "Agachamento", "muscle_group_id": 3},
    {"name": "Desenvolvimento militar", "muscle_group_id": 4},
    {"name": "Rosca direta", "muscle_group_id": 5},
    {"name": "Tríceps testa", "muscle_group_id": 6}
]
resp = supabase.table("exercises").insert(exercises).execute()
print("Exercises:", resp.data)

# Inserir uma sessão de treino
from datetime import datetime
session = {"session_date": datetime.now().isoformat()}
resp = supabase.table("sessions").insert(session).execute()
session_id = resp.data[0]["id"]
print("Session:", resp.data)

# Inserir exercícios na sessão
session_exercises = [
    {"session_id": session_id, "exercise_id": 1},
    {"session_id": session_id, "exercise_id": 2}
]
resp = supabase.table("session_exercises").insert(session_exercises).execute()
print("Session exercises:", resp.data)

# Inserir sets para o primeiro exercício da sessão
session_exercise_id = resp.data[0]["id"]
sets = [
    {"session_exercise_id": session_exercise_id, "set_number": 1, "weight": 60, "reps": 10},
    {"session_exercise_id": session_exercise_id, "set_number": 2, "weight": 60, "reps": 8}
]
resp = supabase.table("sets").insert(sets).execute()
print("Sets:", resp.data)

import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis do .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Adicionar Nova Sessão de Treino")

# Selecionar data/hora
session_date = st.date_input("Data do treino", value=datetime.now().date())
session_time = st.time_input("Hora do treino", value=datetime.now().time())

# Buscar exercícios disponíveis
exercises_resp = supabase.table("exercises").select("id, name").execute()
exercises = exercises_resp.data or []

# Selecionar exercícios para a sessão
selected_exercises = st.multiselect(
    "Exercícios realizados",
    options=[(e["id"], e["name"]) for e in exercises],
    format_func=lambda x: x[1]
)

session_data = None
if st.button("Criar sessão de treino"):
    # Inserir sessão
    dt = datetime.combine(session_date, session_time)
    resp = supabase.table("sessions").insert({"session_date": dt.isoformat()}).execute()
    if resp.data:
        session_id = resp.data[0]["id"]
        # Inserir exercícios na sessão
        for ex in selected_exercises:
            supabase.table("session_exercises").insert({"session_id": session_id, "exercise_id": ex[0]}).execute()
        st.success("Sessão criada com sucesso!")
        session_data = session_id
    else:
        st.error("Erro ao criar sessão.")

# Se sessão criada, permitir inserir sets para cada exercício
if session_data:
    st.subheader("Adicionar Sets aos Exercícios")
    for ex in selected_exercises:
        st.markdown(f"**{ex[1]}**")
        n_sets = st.number_input(f"Nº de sets para {ex[1]}", min_value=1, max_value=10, value=3, key=f"sets_{ex[0]}")
        for s in range(1, n_sets+1):
            weight = st.number_input(f"Peso (kg) - Set {s}", min_value=0.0, value=0.0, key=f"w_{ex[0]}_{s}")
            reps = st.number_input(f"Reps - Set {s}", min_value=1, value=10, key=f"r_{ex[0]}_{s}")
            if st.button(f"Guardar Set {s} de {ex[1]}", key=f"save_{ex[0]}_{s}"):
                # Buscar session_exercise_id
                se_resp = supabase.table("session_exercises").select("id").eq("session_id", session_data).eq("exercise_id", ex[0]).execute()
                if se_resp.data:
                    se_id = se_resp.data[0]["id"]
                    supabase.table("sets").insert({
                        "session_exercise_id": se_id,
                        "set_number": s,
                        "weight": weight,
                        "reps": reps
                    }).execute()
                    st.success(f"Set {s} guardado!")

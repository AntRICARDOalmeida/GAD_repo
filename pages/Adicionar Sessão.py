
import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Adicionar Nova Sessão de Treino")
session_date = st.date_input("Data do treino", value=datetime.now().date())
session_time = st.time_input("Hora do treino", value=datetime.now().time())

# Buscar exercícios disponíveis
exercises_resp = supabase.table("exercises").select("id, name").order("name").execute()
exercises = exercises_resp.data or []
exercise_options = {e["name"]: e["id"] for e in exercises}

# Estado dinâmico para múltiplos exercícios
if "ex_sections" not in st.session_state:
    st.session_state.ex_sections = [0]

def add_section():
    st.session_state.ex_sections.append(len(st.session_state.ex_sections))

st.subheader("Exercícios da Sessão")
for idx in st.session_state.ex_sections:
    st.markdown(f"### Exercício {idx+1}")
    ex_name = st.selectbox(f"Exercício", list(exercise_options.keys()), key=f"ex_{idx}")
    n_sets = st.number_input(f"Nº de sets", min_value=1, max_value=10, value=3, key=f"sets_{idx}")
    peso = st.number_input(f"Peso (kg)", min_value=0.0, value=0.0, key=f"peso_{idx}")
    st.session_state[f"ex_data_{idx}"] = {
        "exercise_id": exercise_options[ex_name],
        "n_sets": n_sets,
        "peso": peso
    }
if st.button("Adicionar mais um exercício"):
    add_section()

if st.button("Guardar sessão de treino"):
    dt = datetime.combine(session_date, session_time)
    resp = supabase.table("sessions").insert({"session_date": dt.isoformat()}).execute()
    if resp.data:
        session_id = resp.data[0]["id"]
        for idx in st.session_state.ex_sections:
            ex_data = st.session_state.get(f"ex_data_{idx}")
            if not ex_data:
                continue
            se_resp = supabase.table("session_exercises").insert({
                "session_id": session_id,
                "exercise_id": ex_data["exercise_id"]
            }).execute()
            if se_resp.data:
                se_id = se_resp.data[0]["id"]
                for s in range(1, int(ex_data["n_sets"])+1):
                    supabase.table("sets").insert({
                        "session_exercise_id": se_id,
                        "set_number": s,
                        "weight": ex_data["peso"]
                    }).execute()
        st.success("Sessão criada com sucesso!")
        # Limpar estado
        st.session_state.ex_sections = [0]
        for k in list(st.session_state.keys()):
            if k.startswith("ex_data_"):
                del st.session_state[k]
    else:
        st.error("Erro ao criar sessão.")

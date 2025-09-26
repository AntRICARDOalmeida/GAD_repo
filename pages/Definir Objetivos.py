import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

st.title("Definir Objetivos Semanais de Sets por Grupo Muscular")

# Ligação à BD
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

groups = supabase.table("muscle_groups").select("id, name").order("name").execute().data or []
obj_table = "muscle_group_goals"
try:
    goals = supabase.table(obj_table).select("muscle_group_id, weekly_sets_goal").execute().data or []
except Exception:
    goals = []
goals_dict = {g["muscle_group_id"]: g["weekly_sets_goal"] for g in goals}

with st.form("definir_objetivos"):
    new_goals = {}
    for g in groups:
        val = st.number_input(f"Objetivo de sets/semana para {g['name']}", min_value=0, value=goals_dict.get(g["id"], 10), key=f"goal_{g['id']}")
        new_goals[g["id"]] = val
    submitted = st.form_submit_button("Guardar objetivos")
    if submitted:
        for gid, sets_goal in new_goals.items():
            existing = supabase.table(obj_table).select("*").eq("muscle_group_id", gid).execute().data
            if existing:
                supabase.table(obj_table).update({"weekly_sets_goal": sets_goal}).eq("muscle_group_id", gid).execute()
            else:
                supabase.table(obj_table).insert({"muscle_group_id": gid, "weekly_sets_goal": sets_goal}).execute()
        st.success("Objetivos atualizados!")

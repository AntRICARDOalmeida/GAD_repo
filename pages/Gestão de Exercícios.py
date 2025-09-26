import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Gestão de Exercícios e Grupos Musculares")
st.header("Grupos Musculares")
with st.form("add_muscle_group"):
    new_group = st.text_input("Novo grupo muscular")
    submitted = st.form_submit_button("Adicionar grupo")
    if submitted and new_group:
        resp = supabase.table("muscle_groups").insert({"name": new_group}).execute()
        if resp.data:
            st.success(f"Grupo '{new_group}' adicionado!")
        else:
            st.error("Erro ao adicionar grupo.")
groups = supabase.table("muscle_groups").select("id, name").order("name").execute().data or []
st.table(groups)
st.header("Exercícios")
with st.form("add_exercise"):
    new_exercise = st.text_input("Nome do exercício")
    group_options = {g["name"]: g["id"] for g in groups}
    group_selected = st.selectbox("Grupo muscular", list(group_options.keys()))
    submitted = st.form_submit_button("Adicionar exercício")
    if submitted and new_exercise:
        resp = supabase.table("exercises").insert({
            "name": new_exercise,
            "muscle_group_id": group_options[group_selected]
        }).execute()
        if resp.data:
            st.success(f"Exercício '{new_exercise}' adicionado!")
        else:
            st.error("Erro ao adicionar exercício.")
exs = supabase.table("exercises").select("id, name, muscle_group_id").order("name").execute().data or []
for e in exs:
    e["grupo_muscular"] = next((g["name"] for g in groups if g["id"] == e["muscle_group_id"]), "-")
st.table([{k: e[k] for k in ("id", "name", "grupo_muscular")} for e in exs])

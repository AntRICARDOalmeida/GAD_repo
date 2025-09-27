import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Gestão de Exercícios e Grupos Musculares")

# --- Grupos Musculares ---
st.header("Grupos Musculares")

# Adicionar grupo muscular
with st.form("add_muscle_group"):
    new_group = st.text_input("Novo grupo muscular")
    submitted = st.form_submit_button("Adicionar grupo")
    if submitted and new_group:
        try:
            resp = supabase.table("muscle_groups").insert({"name": new_group}).execute()
            if resp.data:
                st.success(f"Grupo '{new_group}' adicionado!")
                st.rerun()
            else:
                st.error("Erro ao adicionar grupo.")
        except Exception as e:
            st.error(f"Erro: {str(e)}")

# Listar e permitir remoção de grupos musculares
groups = supabase.table("muscle_groups").select("id, name").order("name").execute().data or []

if groups:
    st.subheader("Grupos Musculares Existentes")
    for group in groups:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text(f"{group['name']} (ID: {group['id']})")
        with col2:
            if st.button(f"🗑️", key=f"del_group_{group['id']}", help=f"Remover grupo '{group['name']}'"):
                try:
                    # Verificar se o grupo tem exercícios associados
                    associated_exercises = supabase.table("exercise_muscle_groups").select("exercise_id").eq("muscle_group_id", group['id']).execute().data
                    if associated_exercises:
                        st.error(f"Não é possível remover o grupo '{group['name']}' porque tem exercícios associados.")
                    else:
                        # Remover o grupo
                        supabase.table("muscle_groups").delete().eq("id", group['id']).execute()
                        st.success(f"Grupo '{group['name']}' removido!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro ao remover grupo: {str(e)}")
else:
    st.info("Nenhum grupo muscular encontrado.")

# --- Exercícios ---
st.header("Exercícios")

# Adicionar exercício
with st.form("add_exercise"):
    new_exercise = st.text_input("Nome do exercício")
    if groups:
        selected_groups = st.multiselect(
            "Grupos musculares (pode selecionar vários)",
            options=[g["name"] for g in groups],
            help="Selecione um ou mais grupos musculares que este exercício trabalha"
        )
    else:
        st.warning("Precisa de ter pelo menos um grupo muscular para criar exercícios.")
        selected_groups = []
    
    submitted = st.form_submit_button("Adicionar exercício")
    if submitted and new_exercise and selected_groups:
        try:
            # Primeiro, adicionar o exercício
            resp = supabase.table("exercises").insert({"name": new_exercise}).execute()
            if resp.data:
                exercise_id = resp.data[0]["id"]
                
                # Depois, associar aos grupos musculares selecionados
                group_dict = {g["name"]: g["id"] for g in groups}
                for group_name in selected_groups:
                    group_id = group_dict[group_name]
                    supabase.table("exercise_muscle_groups").insert({
                        "exercise_id": exercise_id,
                        "muscle_group_id": group_id
                    }).execute()
                
                st.success(f"Exercício '{new_exercise}' adicionado com grupos: {', '.join(selected_groups)}!")
                st.rerun()
            else:
                st.error("Erro ao adicionar exercício.")
        except Exception as e:
            st.error(f"Erro: {str(e)}")
    elif submitted and new_exercise and not selected_groups:
        st.error("Deve selecionar pelo menos um grupo muscular.")

# Listar exercícios com grupos musculares e opção de remoção
if groups:
    exs = supabase.table("exercises").select("id, name").order("name").execute().data or []
    
    if exs:
        st.subheader("Exercícios Existentes")
        for ex in exs:
            # Buscar grupos musculares do exercício
            ex_groups = supabase.table("exercise_muscle_groups").select("muscle_group_id").eq("exercise_id", ex["id"]).execute().data or []
            group_names = []
            for eg in ex_groups:
                group_name = next((g["name"] for g in groups if g["id"] == eg["muscle_group_id"]), "?")
                group_names.append(group_name)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"{ex['name']} → {', '.join(group_names) if group_names else 'Sem grupos'}")
            with col2:
                if st.button(f"🗑️", key=f"del_ex_{ex['id']}", help=f"Remover exercício '{ex['name']}'"):
                    try:
                        # Verificar se o exercício está sendo usado em sessões
                        sessions_using = supabase.table("session_exercises").select("id").eq("exercise_id", ex['id']).execute().data
                        if sessions_using:
                            st.error(f"Não é possível remover o exercício '{ex['name']}' porque está sendo usado em sessões.")
                        else:
                            # Remover associações com grupos musculares
                            supabase.table("exercise_muscle_groups").delete().eq("exercise_id", ex['id']).execute()
                            # Remover o exercício
                            supabase.table("exercises").delete().eq("id", ex['id']).execute()
                            st.success(f"Exercício '{ex['name']}' removido!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao remover exercício: {str(e)}")
    else:
        st.info("Nenhum exercício encontrado.")
else:
    st.info("Crie grupos musculares primeiro para poder adicionar exercícios.")

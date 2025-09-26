from supabase import create_client, Client
import streamlit as st
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


supabase = get_supabase_client()

st.title("Ligação ao Supabase")
try:
    user_tables = supabase.table("exercises").select("*").limit(1).execute()
    st.success("Ligação bem sucedida! Tabela 'exercises' acessível.")
    st.write(user_tables.data)
except Exception as e:
    st.error(f"Erro na ligação ao Supabase: {e}")

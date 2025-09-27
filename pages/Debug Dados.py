import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import pandas as pd

st.title("Debug: Dados das Sessões e Sets")

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

sessions = supabase.table("sessions").select("*").order("session_date", desc=True).execute().data or []
st.subheader("Sessions")
st.dataframe(pd.DataFrame(sessions))

se = supabase.table("session_exercises").select("*").execute().data or []
st.subheader("Session Exercises")
st.dataframe(pd.DataFrame(se))

sets = supabase.table("sets").select("*").execute().data or []
st.subheader("Sets")
st.dataframe(pd.DataFrame(sets))

import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px


st.title("Dashboard de Treinos")
st.write("Bem-vindo à tua app de registo e análise de treinos!")
st.info("Seleciona uma página no menu à esquerda para começar.")

st.title("Dashboard de Treinos")

# --- Ligação à BD ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Carregar grupos e objetivos para o gráfico ---
groups = supabase.table("muscle_groups").select("id, name").order("name").execute().data or []
obj_table = "muscle_group_goals"
try:
	goals = supabase.table(obj_table).select("muscle_group_id, weekly_sets_goal").execute().data or []
except Exception:
	goals = []
goals_dict = {g["muscle_group_id"]: g["weekly_sets_goal"] for g in goals}


# --- Gráfico de barras: volume semanal por grupo muscular com navegação de semanas ---
st.header("Volume semanal por grupo muscular")

# Estado para navegação de semanas
if "week_offset" not in st.session_state:
	st.session_state.week_offset = 0

# Controles de navegação e seleção de número de semanas
col1, col2, col3, col4 = st.columns([1,2,1,1])
with col1:
	if st.button("← Semana anterior"):
		st.session_state.week_offset -= 1
with col3:
	if st.button("Semana seguinte →"):
		st.session_state.week_offset += 1
with col4:
	num_weeks = st.selectbox("Nº de semanas", options=[1, 2, 3, 4], index=0, key="num_weeks")

# Cálculo das datas (semanas começam no domingo)
hoje = datetime.now().date()
days_since_sunday = (hoje.weekday() + 1) % 7
inicio_primeira_semana = hoje - timedelta(days=days_since_sunday) + timedelta(weeks=st.session_state.week_offset)
inicio_semana = inicio_primeira_semana
fim_semana = inicio_primeira_semana + timedelta(days=(num_weeks * 7) - 1)

# Display do período
if num_weeks == 1:
	st.write(f"Semana: {inicio_semana.strftime('%d/%m/%Y')} a {fim_semana.strftime('%d/%m/%Y')}")
else:
	st.write(f"Período: {inicio_semana.strftime('%d/%m/%Y')} a {fim_semana.strftime('%d/%m/%Y')} ({num_weeks} semanas)")

# Buscar todas as sessões e filtrar por data em Python
import dateutil.parser
sessions = supabase.table("sessions").select("id, session_date").execute().data or []
sessions_semana = []
for s in sessions:
	try:
		data_sessao = dateutil.parser.isoparse(s["session_date"]).date()
		if inicio_semana <= data_sessao <= fim_semana:
			sessions_semana.append(s)
	except Exception:
		pass
session_ids = [s["id"] for s in sessions_semana]
se = supabase.table("session_exercises").select("id, exercise_id, session_id").in_("session_id", session_ids).execute().data or []
se_ids = [x["id"] for x in se]
sets = supabase.table("sets").select("id, session_exercise_id").in_("session_exercise_id", se_ids).execute().data or []
exercises = supabase.table("exercises").select("id, muscle_group_id").execute().data or []
ex_dict = {e["id"]: e["muscle_group_id"] for e in exercises}
mg_dict = {g["id"]: g["name"] for g in groups}

sets_por_grupo = {g["name"]: 0 for g in groups}
for s in sets:
	se_id = s["session_exercise_id"]
	ex_id = next((x["exercise_id"] for x in se if x["id"] == se_id), None)
	mg_id = ex_dict.get(ex_id)
	if mg_id:
		sets_por_grupo[mg_dict[mg_id]] += 1

bar_data = pd.DataFrame({
	"Grupo Muscular": list(sets_por_grupo.keys()),
	"Sets Realizados": list(sets_por_grupo.values()),
	"Objetivo": [goals_dict.get(g["id"], 0) * num_weeks for g in groups]  # Multiplicar objetivo pelo número de semanas
})


fig = px.bar(
    bar_data,
    y="Grupo Muscular",
    x="Sets Realizados",
    orientation="h",
    text="Sets Realizados",
    color_discrete_sequence=["#1f77b4"]  # Cor azul sólida
)
for idx, row in bar_data.iterrows():
    fig.add_shape(
        type="line",
        x0=row["Objetivo"], x1=row["Objetivo"],
        y0=idx-0.4, y1=idx+0.4,
        line=dict(color="red", width=2, dash="dash"),
    )
    fig.add_annotation(
        x=row["Objetivo"], y=idx,
        text=f"Obj: {row['Objetivo']}",
        showarrow=False,
        font=dict(color="red", size=10),
        xanchor="left"
    )
fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    showlegend=False,
    height=400,
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(size=12)
)
st.plotly_chart(fig, use_container_width=True)

# --- Resumo dos últimos 5 treinos ---
st.header("Últimos 5 treinos: resumo por grupo muscular")
ultimas_sessoes = sorted(sessions, key=lambda x: x["session_date"], reverse=True)[:5]
if ultimas_sessoes:
	resumo = []
	for sess in ultimas_sessoes:
		sess_id = sess["id"]
		data = sess["session_date"][:10]
		se_sess = [x for x in se if x["session_id"] == sess_id]
		grupos = {}
		for se_item in se_sess:
			ex_id = se_item["exercise_id"]
			mg_id = ex_dict.get(ex_id)
			grupo_nome = mg_dict.get(mg_id, "-")
			n_sets = len([s for s in sets if s["session_exercise_id"] == se_item["id"]])
			if grupo_nome in grupos:
				grupos[grupo_nome] += n_sets
			else:
				grupos[grupo_nome] = n_sets
		resumo.append({
			"Data": data,
			"Grupos Musculares": ", ".join(grupos.keys()),
			"Sets por Grupo": ", ".join(f"{g}: {n}" for g, n in grupos.items())
		})
	import pandas as pd
	st.dataframe(pd.DataFrame(resumo))
else:
	st.info("Ainda não existem sessões registadas.")

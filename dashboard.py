import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
		page_title="Dashboard",
		page_icon=":bar_chart:",
		layout="wide"
	)
	
@st.cache
def get_data_from_excel():
	print('Leyendo documento...')
	df = pd.read_excel(
			io="BASE DE DATOS ADEI 2022 (005).xlsx",
			engine='openpyxl',
			sheet_name='Respuestas de formulario 1',
			skiprows=5,
			usecols='A:O',
		)
	#Add 'Hour' column to dataframe
	df['Month'] = pd.to_datetime(df['Marca temporal']).dt.month
	print(df['Nombres '])
	return df

df = get_data_from_excel()

st.sidebar.header("Filtros")
nombre = st.sidebar.multiselect(
		label="Nombre",
		options=df["Nombres "].unique(),
		default=df["Nombres "].unique()
)

departamento = st.sidebar.multiselect(
		label="Departamento",
		options=df["Departamento de residencia"].unique(),
		default=df["Departamento de residencia"].unique()
)

postgrado = st.sidebar.multiselect(
		label="Postgrado",
		options=df["Postgrado (s) obtenido (s)"].unique(),
		default=df["Postgrado (s) obtenido (s)"].unique()
)

seguimiento = st.sidebar.multiselect(
		label="Seguimiento del proyecto",
		options=df["Seguimiento del proyecto"].unique(),
		default=df["Seguimiento del proyecto"].unique()
)

df_selection = df.query(
		"`Nombres ` in @nombre and `Departamento de residencia` in @departamento and `Postgrado (s) obtenido (s)` in @postgrado and `Seguimiento del proyecto` in @seguimiento"
)

# -- MainPage --

st.title("Edu Vida")
st.markdown("##")

#Get the total unique values of the `Nombres ` column
total_estudiantes = int(df["Nombres "].nunique())
#Get the unique values of the total_estudiantes_postgrado column
total_estudiantes_titulo = int(df_selection["Título del proyecto con que se graduó"].nunique())
#Get the unique values of the total_estudiantes_departamento column
total_estudiantes_departamento = int(df_selection["Departamento de residencia"].nunique())

left_column, middle_column, right_column = st.columns(3)

with left_column:
	st.subheader("Estudiantes")
	st.markdown(f"**{total_estudiantes}**")

with middle_column:
	st.subheader("Postgrados")
	st.markdown(f"**{total_estudiantes_titulo}**")

with right_column:
	st.subheader("Departamentos")
	st.markdown(f"**{total_estudiantes_departamento}**")

st.markdown("---")

#Primer chart - estudiantes por departamento
estudiantes_por_departamento = df_selection.groupby("Departamento de residencia")["Nombres "].nunique().reset_index()

estudiantes_departamento_chart = px.bar(
		data_frame=estudiantes_por_departamento,
		x="Nombres ",
		y="Departamento de residencia",
		title="Estudiantes por departamento",
		orientation="h",
		color_discrete_sequence=["#0083B8"] * len(estudiantes_por_departamento),
		template="plotly_white",

)

estudiantes_departamento_chart.update_layout(
	plot_bgcolor="rgba(0,0,0,0)",
	xaxis=dict(
		showgrid=False,
		showline=False,
		showticklabels=True,
		linecolor="rgb(204, 204, 204)",
		linewidth=2,
		ticks="outside",
	),
)

# st.plotly_chart(estudiantes_departamento_chart)

#Segundo Chart - Estudiantes por postgrado
postragos_por_mes = (
	df_selection.groupby(by=["Month"]).sum()[["Postgrado (s) obtenido (s)"]].sort_values(by="Month", ascending=False)
)

postragos_mes_chart = px.bar(
	postragos_por_mes,
	x="Postgrado (s) obtenido (s)",
	y=postragos_por_mes.index,
	labels={"Month": "Mes"},
	title="Postgrados por mes",
	orientation="v",
	color_discrete_sequence=["#0083b8"] * len(postragos_por_mes),
	template="plotly_white",
)

postragos_mes_chart.update_layout(
	xaxis=dict(tickmode="linear"),
	plot_bgcolor="rgba(0,0,0,0)",
	yaxis=(dict(showgrid=False)),
)

# st.plotly_chart(postragos_mes_chart)

left_column, right_column = st.columns(2)
left_column.plotly_chart(estudiantes_departamento_chart, use_container_width=True)
right_column.plotly_chart(postragos_mes_chart, use_container_width=True)

# Hidde STREAMLIT style
hide_streamlit_style = """ 
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("---")

st.dataframe(df_selection)
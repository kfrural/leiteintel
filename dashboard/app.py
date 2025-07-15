import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="LeiteIntel Dashboard", layout="wide")

df = pd.read_csv("data/leiteintel_base_ampliada.csv")

st.title("📊 LeiteIntel — Painel de Inteligência de Produção de Leite")

# Filtros
estado = st.sidebar.selectbox("Escolha um estado:", df["estado"].unique())
ano = st.sidebar.slider("Ano", int(df["ano"].min()), int(df["ano"].max()), step=1)

filtro = df[(df["estado"] == estado) & (df["ano"] == ano)]

st.subheader(f"📍 Estado: {estado} | Ano: {ano}")
st.metric("Produção Média", f'{filtro["producao_litros"].mean():,.0f} litros')
st.metric("Preço Médio", f'R$ {filtro["preco_litro"].mean():.2f}')

# Gráfico de linha por mês
fig, ax = plt.subplots()
sns.lineplot(data=filtro, x="mes", y="producao_litros", hue="tipo_producao", marker="o", ax=ax)
plt.title("Produção Mensal por Tipo de Produção")
st.pyplot(fig)

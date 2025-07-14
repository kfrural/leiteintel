import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 LeiteIntel — Painel de Inteligência de Produção de Leite")

df = pd.read_csv("data/leite_data_brasil.csv")
estado = st.selectbox("Escolha um estado:", df["estado"].unique())
filtro = df[df["estado"] == estado]

st.write(f"### Estatísticas para {estado}")
st.write(filtro.describe())

fig, ax = plt.subplots()
sns.lineplot(data=filtro, x="ano", y="producao_litros", hue="mes", palette="viridis", ax=ax)
plt.title("Produção ao longo dos anos")
st.pyplot(fig)

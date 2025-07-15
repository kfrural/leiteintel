import streamlit as st

def mostrar_sidebar(df):
    estado = st.sidebar.selectbox("Escolha o estado:", sorted(df["estado"].unique()))
    ano = st.sidebar.slider("Escolha o ano:", int(df["ano"].min()), int(df["ano"].max()))
    opcao = st.sidebar.radio("O que deseja visualizar?", ["📊 Visão Geral", "📋 Tabelas", "🔮 Previsão", "📄 Gerar Relatório PDF"])
    return estado, ano, opcao

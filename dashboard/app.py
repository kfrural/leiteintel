# app.py

import sys
import os
import pandas as pd
import streamlit as st

# Ajusta o path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from componentes import mostrar_sidebar
from graficos import grafico_producao
from modelos import treinar_modelo
from relatorios import gerar_pdf_resumo

st.set_page_config(page_title="LeiteIntel Dashboard", layout="wide")

# === PATHS DOS ARQUIVOS ===
DATA_RAW = "data/leiteintel_base_ampliada.csv"           # arquivo raw na pasta data/
DATA_CLEAN = "data/processed/leiteintel_base_limpa.csv"  # arquivo limpo na pasta data/processed/

# === FUNÇÃO PARA GERAR BASE LIMPA ===
def gerar_base_limpa():
    if not os.path.exists(DATA_RAW):
        st.error(f"Arquivo raw '{DATA_RAW}' não encontrado. Coloque o arquivo na pasta correta.")
        st.stop()

    df = pd.read_csv(DATA_RAW)
    df = df.dropna()
    df["mes"] = df["mes"].astype(str)

    os.makedirs(os.path.dirname(DATA_CLEAN), exist_ok=True)
    df.to_csv(DATA_CLEAN, index=False)
    print("Base limpa gerada com sucesso!")

# === VERIFICAÇÃO E GERAÇÃO DA BASE LIMPA ===
if not os.path.exists(DATA_CLEAN):
    gerar_base_limpa()

# === CARREGAR BASE ===
if not os.path.exists(DATA_CLEAN):
    st.error(f"Arquivo limpo '{DATA_CLEAN}' não encontrado e não foi possível gerar a base limpa.")
    st.stop()

df = pd.read_csv(DATA_CLEAN)

# === SIDEBAR ===
estado, ano, opcao = mostrar_sidebar(df)

# === FILTRO DE DADOS ===
filtro = df[(df["estado"] == estado) & (df["ano"] == ano)]

# === MÉTRICAS ===
prod_medio = filtro["producao_litros"].mean()
preco_medio = filtro["preco_litro"].mean()
temp_media = filtro["temperatura_media"].mean()
chuva_media = filtro["chuvas_mm"].mean()

# === VISÕES ===
if opcao == "📊 Visão Geral":
    st.title("📊 LeiteIntel — Painel de Inteligência de Produção de Leite")
    st.markdown(f"""
O **LeiteIntel** é um sistema de apoio à decisão para análise da cadeia produtiva do leite.
Você está visualizando os dados de **{estado} - {ano}**.
""")
    st.pyplot(grafico_producao(filtro))

elif opcao == "📋 Tabelas":
    st.title("📋 Análise de Tabelas")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Produção Média", f'{prod_medio:,.0f} litros')
    col2.metric("Preço Médio", f'R$ {preco_medio:.2f}')
    col3.metric("Temperatura Média", f'{temp_media:.1f} °C')
    col4.metric("Chuva Média", f'{chuva_media:.1f} mm')

    st.markdown("### 🧮 Médias por Tipo de Produção")
    tabela_producao = filtro.groupby("tipo_producao")[["producao_litros", "preco_litro"]].mean().round(1).reset_index()
    st.dataframe(tabela_producao)

    st.markdown("### 🧪 Médias por Uso de Tecnologia")
    tabela_tecnologia = filtro.groupby("uso_tecnologia")[["producao_litros", "preco_litro"]].mean().round(1).reset_index()
    st.dataframe(tabela_tecnologia)

elif opcao == "🔮 Previsão":
    st.title("🔮 Previsão de Produção de Leite")
    st.markdown("Faça simulações com variáveis para prever a produção estimada.")

    col5, col6 = st.columns(2)
    temperatura_input = col5.slider("Temperatura média (°C)", 10.0, 40.0, float(round(temp_media, 1)))
    chuva_input = col6.slider("Chuvas (mm)", 0.0, 300.0, float(round(chuva_media, 1)))

    col7, col8 = st.columns(2)
    preco_input = col7.slider("Preço por litro (R$)", 1.0, 6.0, float(round(preco_medio, 2)))
    tipo_input = col8.selectbox("Tipo de Produção", df["tipo_producao"].unique())

    modelo = treinar_modelo(df[["temperatura_media", "chuvas_mm", "preco_litro", "tipo_producao", "producao_litros"]])

    entrada = pd.DataFrame([{
        "temperatura_media": temperatura_input,
        "chuvas_mm": chuva_input,
        "preco_litro": preco_input,
        "tipo_producao": tipo_input
    }])

    producao_prevista = modelo.predict(entrada)[0]
    st.success(f"📈 Produção prevista: **{int(producao_prevista):,} litros**")

elif opcao == "📄 Gerar Relatório PDF":
    st.title("📄 Gerar Relatório Interpretado")

    resumo = f"""
No período analisado, o estado de {estado} apresentou uma produção média de {int(prod_medio):,} litros de leite,
com preço médio de R$ {preco_medio:.2f}/litro. A temperatura média foi de {temp_media:.1f} °C e a precipitação média foi de {chuva_media:.1f} mm.

Este relatório visa auxiliar produtores e técnicos na tomada de decisão com base em dados históricos.
"""
    st.markdown("### Texto que será incluído no PDF:")
    st.code(resumo)

    if st.button("📥 Gerar PDF"):
        caminho_pdf = f"relatorios/relatorio_{estado}_{ano}.pdf"
        os.makedirs(os.path.dirname(caminho_pdf), exist_ok=True)
        gerar_pdf_resumo(resumo, caminho_pdf)
        with open(caminho_pdf, "rb") as file:
            st.download_button(
                label="📄 Baixar PDF",
                data=file,
                file_name=f"relatorio_leiteintel_{estado}_{ano}.pdf",
                mime="application/pdf"
            )

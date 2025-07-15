import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import tempfile
import os

st.set_page_config(page_title="LeiteIntel Dashboard", layout="wide")

# === CARREGAR DADOS ===
df = pd.read_csv("data/leiteintel_base_ampliada.csv")

# === SIDEBAR ===
st.sidebar.title("🔧 Configurações")

estado = st.sidebar.selectbox("Escolha o estado:", sorted(df["estado"].unique()))
ano = st.sidebar.slider("Escolha o ano:", int(df["ano"].min()), int(df["ano"].max()), step=1)

opcao = st.sidebar.radio("O que deseja visualizar?", ["📊 Visão Geral", "📋 Tabelas", "🔮 Previsão", "📄 Gerar Relatório PDF"])

# === FILTRO DE DADOS ===
filtro = df[(df["estado"] == estado) & (df["ano"] == ano)]

# === MÉTRICAS ===
prod_medio = filtro["producao_litros"].mean()
preco_medio = filtro["preco_litro"].mean()
temp_media = filtro["temperatura_media"].mean()
chuva_media = filtro["chuvas_mm"].mean()

# === FUNÇÃO GRÁFICO ===
def grafico_producao():
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=filtro, x="mes", y="producao_litros", hue="tipo_producao", marker="o", ax=ax)
    plt.title("Produção Mensal por Tipo de Produção")
    plt.xlabel("Mês")
    plt.ylabel("Produção (litros)")
    plt.legend(title="Tipo de Produção", bbox_to_anchor=(1.05, 1), loc='upper left')
    return fig

# === VISÃO GERAL ===
if opcao == "📊 Visão Geral":
    st.title("📊 LeiteIntel — Painel de Inteligência de Produção de Leite")
    st.markdown(f"""
O **LeiteIntel** é um sistema de apoio à decisão voltado para análise da cadeia produtiva do leite no Brasil.  
Você está visualizando os dados de **{estado} - {ano}**.
""")
    st.pyplot(grafico_producao())

# === TABELAS ===
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

# === PREVISÃO ===
elif opcao == "🔮 Previsão":
    st.title("🔮 Previsão de Produção de Leite")
    st.markdown("Faça simulações com variáveis para prever a produção estimada.")

    col5, col6 = st.columns(2)
    temperatura_input = col5.slider("Temperatura média (°C)", 10.0, 40.0, float(round(temp_media, 1)))
    chuva_input = col6.slider("Chuvas (mm)", 0.0, 300.0, float(round(chuva_media, 1)))

    col7, col8 = st.columns(2)
    preco_input = col7.slider("Preço por litro (R$)", 1.0, 6.0, float(round(preco_medio, 2)))
    tipo_input = col8.selectbox("Tipo de Produção", df["tipo_producao"].unique())

    # Modelo
    df_modelo = df[["temperatura_media", "chuvas_mm", "preco_litro", "tipo_producao", "producao_litros"]]
    X = df_modelo.drop("producao_litros", axis=1)
    y = df_modelo["producao_litros"]

    preproc = ColumnTransformer([
        ("onehot", OneHotEncoder(), ["tipo_producao"])
    ], remainder='passthrough')

    modelo = Pipeline([
        ("prep", preproc),
        ("reg", LinearRegression())
    ])
    modelo.fit(X, y)

    entrada = pd.DataFrame([{
        "temperatura_media": temperatura_input,
        "chuvas_mm": chuva_input,
        "preco_litro": preco_input,
        "tipo_producao": tipo_input
    }])

    producao_prevista = modelo.predict(entrada)[0]
    st.success(f"📈 Produção prevista: **{int(producao_prevista):,} litros**")

# === RELATÓRIO PDF ===
elif opcao == "📄 Gerar Relatório PDF":
    st.title("📄 Gerar Relatório PDF")

    tabela_producao = filtro.groupby("tipo_producao")[["producao_litros", "preco_litro"]].mean().round(1).reset_index()
    tabela_tecnologia = filtro.groupby("uso_tecnologia")[["producao_litros", "preco_litro"]].mean().round(1).reset_index()
    fig = grafico_producao()

    # Previsão
    df_modelo = df[["temperatura_media", "chuvas_mm", "preco_litro", "tipo_producao", "producao_litros"]]
    X = df_modelo.drop("producao_litros", axis=1)
    y = df_modelo["producao_litros"]

    modelo = Pipeline([
        ("prep", ColumnTransformer([("onehot", OneHotEncoder(), ["tipo_producao"])], remainder='passthrough')),
        ("reg", LinearRegression())
    ])
    modelo.fit(X, y)
    entrada = pd.DataFrame([{
        "temperatura_media": temp_media,
        "chuvas_mm": chuva_media,
        "preco_litro": preco_medio,
        "tipo_producao": df["tipo_producao"].mode()[0]
    }])
    producao_prevista = modelo.predict(entrada)[0]

    def gerar_relatorio_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="Relatório Analítico - LeiteIntel", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Estado: {estado} | Ano: {ano}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 8, f"""
Este relatório apresenta uma análise da produção de leite no estado de {estado} no ano de {ano}, com base em dados de clima, tecnologia e estratégias de manejo.
Inclui também uma previsão de produção futura.
        """)
        pdf.cell(200, 8, txt=f"• Produção Média: {int(prod_medio):,} litros", ln=True)
        pdf.cell(200, 8, txt=f"• Preço Médio: R$ {preco_medio:.2f}", ln=True)
        pdf.cell(200, 8, txt=f"• Temperatura Média: {temp_media:.1f} °C", ln=True)
        pdf.cell(200, 8, txt=f"• Chuva Média: {chuva_media:.1f} mm", ln=True)
        pdf.cell(200, 8, txt=f"• Previsão de Produção: {int(producao_prevista):,} litros", ln=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name, bbox_inches='tight')
            pdf.image(tmpfile.name, x=10, y=None, w=190)
            tmpfile.close()
            os.unlink(tmpfile.name)

        pdf.add_page()
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="Médias por Tipo de Produção", ln=True)
        pdf.set_font("Arial", size=11)
        for i, row in tabela_producao.iterrows():
            pdf.cell(200, 8, txt=f"{row['tipo_producao']}: {row['producao_litros']} litros, R$ {row['preco_litro']}/litro", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="Médias por Uso de Tecnologia", ln=True)
        pdf.set_font("Arial", size=11)
        for i, row in tabela_tecnologia.iterrows():
            pdf.cell(200, 8, txt=f"{row['uso_tecnologia']}: {row['producao_litros']} litros, R$ {row['preco_litro']}/litro", ln=True)

        return pdf

    if st.button("📥 Gerar e Baixar Relatório PDF"):
        relatorio = gerar_relatorio_pdf()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            relatorio.output(tmp_pdf.name)
            with open(tmp_pdf.name, "rb") as file:
                st.download_button(
                    label="📥 Baixar Relatório PDF",
                    data=file,
                    file_name=f"relatorio_leiteintel_{estado}_{ano}.pdf",
                    mime="application/pdf"
                )
            os.unlink(tmp_pdf.name)

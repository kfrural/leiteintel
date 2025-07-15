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

def gerar_texto_analitico(estado, ano, prod_medio, preco_medio, temp_media, chuva_media, producao_prevista=None):
    texto = f"""
No ano de {ano}, o estado de {estado} apresentou uma produção média de leite de aproximadamente {int(prod_medio):,} litros.  
O preço médio pago por litro foi de R$ {preco_medio:.2f}, indicando um mercado {"favorável" if preco_medio > 3.5 else "moderado"} para os produtores.  

As condições climáticas mostraram uma temperatura média de {temp_media:.1f} °C e um índice pluviométrico de {chuva_media:.1f} mm, fatores importantes que influenciam diretamente na produção.

"""
    if producao_prevista:
        texto += f"\nCom base nas variáveis observadas, estima-se uma produção futura de aproximadamente {int(producao_prevista):,} litros, o que pode indicar uma tendência de {'crescimento' if producao_prevista > prod_medio else 'estabilidade ou queda'} na produção para o próximo período.\n"

    texto += """
Esta análise auxilia técnicos e produtores a entenderem melhor as condições atuais e planejarem estratégias para otimizar a produção e a rentabilidade na cadeia do leite.
"""
    return texto.strip()


if opcao == "📊 Visão Geral":
    st.title("📊 LeiteIntel — Painel de Inteligência de Produção de Leite")
    st.markdown(f"""
O **LeiteIntel** é um sistema de apoio à decisão voltado para análise da cadeia produtiva do leite no Brasil.  
Você está visualizando os dados de **{estado} - {ano}**.
""")
    st.pyplot(grafico_producao())

elif opcao == "📋 Tabelas":
    st.title("📋 Análise de Tabelas")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Produção Média", f'{prod_medio:,.0f} litros')
    col2.metric("Preço Médio", f'R$ {preco_medio:.2f}')
    col3.metric("Temperatura Média", f'{temp_media:.1f} °C')
    col4.metric("Chuva Média", f'{chuva_media:.1f} mm')

    st.markdown("### 🧮 Médias por Tipo de Produção")
    tabela_producao = filtro.groupby("tipo_producao")[["producao_litros", "preco_litro"]].mean().round(1).reset_index()
    tabela_producao = tabela_producao.rename(columns={
        "tipo_producao": "Tipo de Produção",
        "producao_litros": "Produção / litros",
        "preco_litro": "Preço / R$"
    })
    st.dataframe(tabela_producao)

    st.markdown("### 🧪 Médias por Uso de Tecnologia")
    tabela_tecnologia = filtro.groupby("uso_tecnologia")[["producao_litros", "preco_litro"]].mean().round(1).reset_index()
    tabela_tecnologia = tabela_tecnologia.rename(columns={
        "uso_tecnologia": "Uso de Tecnologia",
        "producao_litros": "Produção / litros",
        "preco_litro": "Preço / R$"
    })
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

elif opcao == "📄 Gerar Relatório PDF":
    st.title("📄 Personalizar e Gerar Relatório")

    st.markdown("Customize o relatório antes de gerar o PDF com base em seus objetivos.")

    estado_rel = st.selectbox("📍 Escolha o estado para o relatório:", sorted(df["estado"].unique()), index=list(df["estado"].unique()).index(estado))
    ano_rel = st.slider("📅 Escolha o ano:", int(df["ano"].min()), int(df["ano"].max()), value=ano)

    filtro_rel = df[(df["estado"] == estado_rel) & (df["ano"] == ano_rel)]

    prod_medio = filtro_rel["producao_litros"].mean()
    preco_medio = filtro_rel["preco_litro"].mean()
    temp_media = filtro_rel["temperatura_media"].mean()
    chuva_media = filtro_rel["chuvas_mm"].mean()

    df_modelo = df[["temperatura_media", "chuvas_mm", "preco_litro", "tipo_producao", "producao_litros"]]
    X = df_modelo.drop("producao_litros", axis=1)
    y = df_modelo["producao_litros"]

    modelo = Pipeline([
        ("prep", ColumnTransformer([("onehot", OneHotEncoder(), ["tipo_producao"])], remainder='passthrough')),
        ("reg", LinearRegression())
    ])
    modelo.fit(X, y)

    tipo_base = filtro_rel["tipo_producao"].mode()[0]
    entrada_rel = pd.DataFrame([{
        "temperatura_media": temp_media,
        "chuvas_mm": chuva_media,
        "preco_litro": preco_medio,
        "tipo_producao": tipo_base
    }])
    producao_prevista = modelo.predict(entrada_rel)[0]

    texto_analitico = gerar_texto_analitico(
        estado_rel, ano_rel, prod_medio, preco_medio, temp_media, chuva_media, producao_prevista
    )

    st.markdown("### 🧩 Escolha o que incluir no relatório:")
    incluir_grafico = st.checkbox("📈 Incluir gráfico de produção", value=True)
    incluir_tab_tipo = st.checkbox("📋 Tabela por tipo de produção", value=True)
    incluir_tab_tecn = st.checkbox("🧪 Tabela por uso de tecnologia", value=True)
    incluir_previsao = st.checkbox("🔮 Incluir previsão de produção", value=True)
    incluir_texto = st.checkbox("📝 Incluir texto analítico", value=True)

    st.markdown("## 👁️ Pré-visualização do Relatório")

    st.markdown(f"**Resumo — {estado_rel} - {ano_rel}:**")
    st.write(f"• Produção média: {int(prod_medio):,} litros")
    st.write(f"• Preço médio: R$ {preco_medio:.2f}")
    st.write(f"• Temperatura média: {temp_media:.1f} °C")
    st.write(f"• Chuva média: {chuva_media:.1f} mm")

    if incluir_texto:
        st.markdown("### 📝 Análise dos Dados")
        st.write(texto_analitico)

    if incluir_grafico:
        fig_rel, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=filtro_rel, x="mes", y="producao_litros", hue="tipo_producao", marker="o", ax=ax)
        plt.title("Produção Mensal por Tipo de Produção")
        plt.xlabel("Mês")
        plt.ylabel("Produção (litros)")
        st.pyplot(fig_rel)
    else:
        fig_rel = None

    if incluir_tab_tipo:
        st.markdown("### 📋 Tabela por Tipo de Produção")
        tabela_producao_rel = filtro_rel.groupby("tipo_producao")[["producao_litros", "preco_litro"]].mean().round(1).reset_index()
        tabela_producao_rel = tabela_producao_rel.rename(columns={
            "tipo_producao": "Tipo de Produção",
            "producao_litros": "Produção / litros",
            "preco_litro": "Preço / R$"
        })
        st.dataframe(tabela_producao_rel)
    else:
        tabela_producao_rel = pd.DataFrame()

    if incluir_tab_tecn:
        st.markdown("### 🧪 Tabela por Uso de Tecnologia")
        tabela_tecnologia_rel = filtro_rel.groupby("uso_tecnologia")[["producao_litros", "preco_litro"]].mean().round(1).reset_index()
        tabela_tecnologia_rel = tabela_tecnologia_rel.rename(columns={
            "uso_tecnologia": "Uso de Tecnologia",
            "producao_litros": "Produção / litros",
            "preco_litro": "Preço / R$"
        })
        st.dataframe(tabela_tecnologia_rel)
    else:
        tabela_tecnologia_rel = pd.DataFrame()

    def gerar_relatorio_pdf_personalizado():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="Relatório Personalizado - LeiteIntel", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Estado: {estado_rel} | Ano: {ano_rel}", ln=True)
        pdf.ln(5)

        if incluir_texto:
            pdf.multi_cell(0, 8, texto_analitico)

        if incluir_grafico and fig_rel:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig_rel.savefig(tmpfile.name, bbox_inches='tight')
                pdf.image(tmpfile.name, x=10, y=None, w=190)
                tmpfile.close()
                os.unlink(tmpfile.name)

        if incluir_tab_tipo and not tabela_producao_rel.empty:
            pdf.add_page()
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(200, 10, txt="Médias por Tipo de Produção", ln=True)
            pdf.set_font("Arial", size=11)
            for i, row in tabela_producao_rel.iterrows():
                pdf.cell(200, 8, txt=f"{row['Tipo de Produção']}: {row['Produção / litros']} litros, R$ {row['Preço / R$']}/litro", ln=True)

        if incluir_tab_tecn and not tabela_tecnologia_rel.empty:
            pdf.ln(5)
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(200, 10, txt="Médias por Uso de Tecnologia", ln=True)
            pdf.set_font("Arial", size=11)
            for i, row in tabela_tecnologia_rel.iterrows():
                pdf.cell(200, 8, txt=f"{row['Uso de Tecnologia']}: {row['Produção / litros']} litros, R$ {row['Preço / R$']}/litro", ln=True)

        return pdf

    st.markdown("---")
    if st.button("📥 Gerar e Baixar Relatório PDF Personalizado"):
        relatorio = gerar_relatorio_pdf_personalizado()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            relatorio.output(tmp_pdf.name)
            with open(tmp_pdf.name, "rb") as file:
                st.download_button(
                    label="📥 Baixar PDF",
                    data=file,
                    file_name=f"relatorio_leiteintel_{estado_rel}_{ano_rel}.pdf",
                    mime="application/pdf"
                )
            os.unlink(tmp_pdf.name)

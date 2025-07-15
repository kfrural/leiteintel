import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="LeiteIntel Dashboard", layout="wide")

# === CARREGAR DADOS ===
df = pd.read_csv("data/leiteintel_base_ampliada.csv")

st.title("📊 LeiteIntel — Painel de Inteligência de Produção de Leite")

# === FILTROS ===
estado = st.sidebar.selectbox("Escolha um estado:", sorted(df["estado"].unique()))
ano = st.sidebar.slider("Ano", int(df["ano"].min()), int(df["ano"].max()), step=1)

filtro = df[(df["estado"] == estado) & (df["ano"] == ano)]

# === MÉTRICAS ===
st.subheader(f"📍 Estado: {estado} | Ano: {ano}")
prod_medio = filtro["producao_litros"].mean()
preco_medio = filtro["preco_litro"].mean()
st.metric("Produção Média", f'{prod_medio:,.0f} litros')
st.metric("Preço Médio", f'R$ {preco_medio:.2f}')

# === GRÁFICO ===
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtro, x="mes", y="producao_litros", hue="tipo_producao", marker="o", ax=ax)
plt.title("Produção Mensal por Tipo de Produção")
plt.xlabel("Mês")
plt.ylabel("Produção (litros)")
plt.legend(title="Tipo de Produção", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)

# === GERAR RELATÓRIO PDF ===
def gerar_relatorio_pdf(estado, ano, prod_medio, preco_medio):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Relatório de Produção de Leite - {estado} - {ano}", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Produção Média: {int(prod_medio):,} litros", ln=True)
    pdf.cell(200, 10, txt=f"Preço Médio: R$ {preco_medio:.2f}", ln=True)
    pdf.ln(10)

    # Adiciona gráfico salvo temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.savefig(tmpfile.name, bbox_inches='tight')
        pdf.image(tmpfile.name, x=10, y=None, w=190)
        tmpfile.close()
        os.unlink(tmpfile.name)  # remove temporário

    return pdf

# === BOTÃO PARA GERAR PDF ===
if st.button("📄 Gerar Relatório em PDF"):
    relatorio = gerar_relatorio_pdf(estado, ano, prod_medio, preco_medio)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        relatorio.output(tmp_pdf.name)
        with open(tmp_pdf.name, "rb") as file:
            st.download_button(
                label="📥 Baixar Relatório PDF",
                data=file,
                file_name=f"relatorio_leiteintel_{estado}_{ano}.pdf",
                mime="application/pdf"
            )
        os.unlink(tmp_pdf.name)  # remove temporário após download

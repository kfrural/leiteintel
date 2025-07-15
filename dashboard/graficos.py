import seaborn as sns
import matplotlib.pyplot as plt

def grafico_producao(filtro):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=filtro, x="mes", y="producao_litros", hue="tipo_producao", marker="o", ax=ax)
    ax.set_title("Produção Mensal por Tipo de Produção")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Produção (litros)")
    return fig

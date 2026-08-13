from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.analysis import associacoes_volume, calcular_kpis, resumo_canal, resumo_categoria, resumo_mensal
from src.data import carregar_dados
from src.metrics import adicionar_metricas


FUNDO = "#0E0A1F"
CARD = "#17112C"
GRADE = "#322752"
TEXTO = "#F7F2FF"
MUTED = "#B6A9C8"
MAGENTA = "#FF4D8D"
AMBAR = "#FFB547"
VIOLETA = "#8A63D2"
VERDE = "#4ED6A3"


def moeda_curta(valor: float) -> str:
    if abs(valor) >= 1_000_000:
        return f"R$ {valor / 1_000_000:.1f} mi".replace(".", ",")
    if abs(valor) >= 1_000:
        return f"R$ {valor / 1_000:.0f} mil".replace(".", ",")
    return f"R$ {valor:,.0f}".replace(",", ".")


def preparar_eixo(eixo):
    eixo.set_facecolor(CARD)
    eixo.tick_params(colors=MUTED, labelsize=9)
    eixo.spines[:].set_visible(False)
    eixo.grid(axis="y", color=GRADE, linewidth=0.7, alpha=0.75)
    eixo.set_axisbelow(True)


def card(figura, x, y, largura, altura, titulo, valor, detalhe, cor):
    figura.add_artist(
        FancyBboxPatch(
            (x, y),
            largura,
            altura,
            transform=figura.transFigure,
            boxstyle="round,pad=0.008,rounding_size=0.015",
            facecolor=CARD,
            edgecolor=GRADE,
            linewidth=1,
        )
    )
    figura.text(x + 0.018, y + altura - 0.035, titulo.upper(), color=MUTED, fontsize=8.5, weight="bold")
    figura.text(x + 0.018, y + 0.045, valor, color=TEXTO, fontsize=21, weight="bold")
    figura.text(x + largura - 0.018, y + 0.05, detalhe, color=cor, fontsize=9, weight="bold", ha="right")


def gerar_dashboard(dados, destino: Path):
    kpis = calcular_kpis(dados)
    mensal = resumo_mensal(dados)
    categorias = resumo_categoria(dados)
    associacoes = associacoes_volume(dados).sort_values("correlacao_spearman")
    canais = resumo_canal(dados)

    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=FUNDO)
    fig.text(0.055, 0.946, "CIÊNCIA DE DADOS APLICADA AO VAREJO DIGITAL", color=MAGENTA, fontsize=9, weight="bold")
    fig.text(0.055, 0.895, "Laboratório de Demanda, Preço e Margem", color=TEXTO, fontsize=27, weight="bold")
    fig.text(0.055, 0.858, "Onde a receita cresce, onde a margem se perde e o que acompanha o volume vendido", color=MUTED, fontsize=11)

    card(fig, 0.055, 0.704, 0.205, 0.112, "Receita líquida", moeda_curta(kpis["receita_liquida"]), "2025", MAGENTA)
    card(fig, 0.278, 0.704, 0.205, 0.112, "Contribuição", moeda_curta(kpis["contribuicao"]), f"{kpis['margem_contribuicao_pct']:.1%}".replace(".", ","), AMBAR)
    card(fig, 0.501, 0.704, 0.205, 0.112, "Unidades líquidas", f"{kpis['unidades_liquidas']:,.0f}".replace(",", "."), f"{kpis['conversao_pct']:.1%} conversão".replace(".", ","), VERDE)
    card(fig, 0.724, 0.704, 0.221, 0.112, "Pedidos", f"{kpis['pedidos']:,.0f}".replace(",", "."), f"{kpis['taxa_devolucao_pct']:.1%} devolução".replace(".", ","), VIOLETA)

    ax_linha = fig.add_axes([0.055, 0.39, 0.555, 0.255])
    preparar_eixo(ax_linha)
    ax_linha.plot(mensal["mes"], mensal["receita_liquida"] / 1_000_000, color=MAGENTA, linewidth=2.7, marker="o", markersize=4.5, label="Receita líquida")
    ax_linha.plot(mensal["mes"], mensal["contribuicao"] / 1_000_000, color=AMBAR, linewidth=2.4, marker="o", markersize=4, label="Contribuição")
    ax_linha.set_title("Receita e contribuição por mês", loc="left", color=TEXTO, fontsize=12, weight="bold", pad=13)
    ax_linha.set_ylabel("R$ milhões", color=MUTED, fontsize=9)
    ax_linha.legend(frameon=False, labelcolor=MUTED, fontsize=8, ncol=2, loc="upper left")
    ax_linha.tick_params(axis="x", rotation=0)
    ax_linha.set_xticks(mensal["mes"])
    ax_linha.set_xticklabels([data.strftime("%b") for data in mensal["mes"]])

    ax_categoria = fig.add_axes([0.645, 0.39, 0.30, 0.255])
    preparar_eixo(ax_categoria)
    categoria_ordem = categorias.sort_values("receita_liquida")
    cores = [VIOLETA] * len(categoria_ordem)
    cores[-1] = MAGENTA
    ax_categoria.barh(categoria_ordem["categoria"], categoria_ordem["receita_liquida"] / 1_000_000, color=cores, height=0.58)
    ax_categoria.set_title("Receita por categoria", loc="left", color=TEXTO, fontsize=12, weight="bold", pad=13)
    ax_categoria.set_xlabel("R$ milhões", color=MUTED, fontsize=9)
    ax_categoria.grid(axis="x", color=GRADE, linewidth=0.7)
    ax_categoria.grid(axis="y", visible=False)

    ax_assoc = fig.add_axes([0.055, 0.085, 0.555, 0.245])
    preparar_eixo(ax_assoc)
    cores_assoc = [VERDE if valor >= 0 else MAGENTA for valor in associacoes["correlacao_spearman"]]
    ax_assoc.barh(associacoes["fator"], associacoes["correlacao_spearman"], color=cores_assoc, height=0.58)
    ax_assoc.axvline(0, color=GRADE, linewidth=1)
    ax_assoc.set_xlim(-1, 1)
    ax_assoc.set_title("Associação de Spearman com o volume líquido", loc="left", color=TEXTO, fontsize=12, weight="bold", pad=13)
    ax_assoc.set_xlabel("Associação, não causalidade", color=MUTED, fontsize=9)
    for indice, valor in enumerate(associacoes["correlacao_spearman"]):
        ax_assoc.text(valor + (0.025 if valor >= 0 else -0.025), indice, f"{valor:.2f}", color=TEXTO, va="center", ha="left" if valor >= 0 else "right", fontsize=8.5, weight="bold")

    ax_canal = fig.add_axes([0.645, 0.085, 0.30, 0.245])
    preparar_eixo(ax_canal)
    x = np.arange(len(canais))
    largura = 0.34
    ax_canal.bar(x - largura / 2, canais["margem_contribuicao_pct"] * 100, largura, color=AMBAR, label="Margem de contribuição")
    ax_canal.bar(x + largura / 2, canais["conversao_pct"] * 100, largura, color=VERDE, label="Conversão")
    ax_canal.set_xticks(x)
    ax_canal.set_xticklabels(canais["canal"])
    ax_canal.set_title("Eficiência por canal", loc="left", color=TEXTO, fontsize=12, weight="bold", pad=13)
    ax_canal.set_ylabel("Percentual", color=MUTED, fontsize=9)
    ax_canal.legend(frameon=False, labelcolor=MUTED, fontsize=7.5, loc="upper right")

    fig.text(0.055, 0.025, "Base sintética reproduzível, criada para estudo de portfólio. Resultados descritivos, não causais.", color=MUTED, fontsize=8)
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, facecolor=FUNDO)
    plt.close(fig)


def gerar_capa_linkedin(dados, destino: Path):
    kpis = calcular_kpis(dados)
    canais = resumo_canal(dados)
    melhor_canal = canais.sort_values("margem_contribuicao_pct", ascending=False).iloc[0]

    fig = plt.figure(figsize=(12, 6.27), dpi=100, facecolor=FUNDO)
    fig.add_artist(FancyBboxPatch((0.045, 0.07), 0.91, 0.86, transform=fig.transFigure, boxstyle="round,pad=0.012,rounding_size=0.03", facecolor=CARD, edgecolor=GRADE, linewidth=1.2, zorder=-1))
    fig.text(0.085, 0.83, "PROJETO DE CIÊNCIA DE DADOS", color=MAGENTA, fontsize=11, weight="bold")
    fig.text(0.085, 0.69, "Demanda, preço\ne margem no e-commerce", color=TEXTO, fontsize=30, weight="bold", linespacing=1.0)
    fig.text(0.085, 0.51, "Um laboratório interativo para investigar volume,\nrentabilidade, curva ABC e cenários comerciais.", color=MUTED, fontsize=13, linespacing=1.45)
    fig.text(0.085, 0.25, moeda_curta(kpis["receita_liquida"]), color=TEXTO, fontsize=23, weight="bold")
    fig.text(0.085, 0.205, "receita líquida simulada", color=MUTED, fontsize=9)
    fig.text(0.33, 0.25, f"{kpis['margem_contribuicao_pct']:.1%}".replace(".", ","), color=AMBAR, fontsize=23, weight="bold")
    fig.text(0.33, 0.205, "margem de contribuição", color=MUTED, fontsize=9)

    ax = fig.add_axes([0.62, 0.20, 0.27, 0.57])
    ax.set_facecolor(CARD)
    meses = resumo_mensal(dados)
    ax.fill_between(range(len(meses)), meses["receita_liquida"] / 1_000_000, color=VIOLETA, alpha=0.18)
    ax.plot(range(len(meses)), meses["receita_liquida"] / 1_000_000, color=MAGENTA, linewidth=3, marker="o", markersize=5)
    ax.set_title("Receita mensal", loc="left", color=TEXTO, fontsize=12, weight="bold", pad=12)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 11])
    ax.set_xticklabels(["jan", "mar", "mai", "jul", "set", "nov", "dez"], color=MUTED, fontsize=8)
    ax.tick_params(axis="y", colors=MUTED, labelsize=8)
    ax.grid(axis="y", color=GRADE, alpha=0.8)
    ax.spines[:].set_visible(False)
    ax.text(0, -0.16, f"{melhor_canal['canal']} lidera a margem de contribuição", transform=ax.transAxes, color=VERDE, fontsize=9, weight="bold")
    fig.text(0.085, 0.105, "Python  |  Pandas  |  Streamlit  |  Plotly  |  Testes automatizados", color=VIOLETA, fontsize=9.5, weight="bold")
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, facecolor=FUNDO)
    plt.close(fig)


if __name__ == "__main__":
    dados = adicionar_metricas(carregar_dados(RAIZ / "data" / "ecommerce_2025.csv"))
    gerar_dashboard(dados, RAIZ / "assets" / "painel_ecommerce.png")
    gerar_capa_linkedin(dados, RAIZ / "assets" / "capa_linkedin.png")
    print("Imagens criadas em assets/")

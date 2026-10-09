from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.analysis import (
    associacoes_volume,
    calcular_kpis,
    curva_abc,
    principais_insights,
    resumo_canal,
    resumo_categoria,
    resumo_desconto,
    resumo_mensal,
)
from src.data import carregar_dados
from src.metrics import adicionar_metricas
from src.simulation import simular_cenario


BASE_DIR = Path(__file__).resolve().parent
CORES = {
    "fundo": "#0E0A1F",
    "card": "#17112C",
    "grade": "#322752",
    "texto": "#F7F2FF",
    "muted": "#B6A9C8",
    "magenta": "#FF4D8D",
    "ambar": "#FFB547",
    "violeta": "#8A63D2",
    "verde": "#4ED6A3",
    "azul": "#56B4FF",
}


def moeda(valor: float) -> str:
    return f"R$ {valor:,.0f}".replace(",", ".")


def numero(valor: float) -> str:
    return f"{valor:,.0f}".replace(",", ".")


def percentual(valor: float) -> str:
    return f"{valor:.1%}".replace(".", ",")


def delta_pct(novo: float, base: float) -> str:
    if base == 0:
        return "0,0%"
    return f"{(novo / base - 1):+.1%}".replace(".", ",")


def aplicar_tema(figura: go.Figure, altura: int = 420) -> go.Figure:
    figura.update_layout(
        height=altura,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, Arial, sans-serif", "color": CORES["texto"], "size": 13},
        title={"font": {"size": 18, "color": CORES["texto"]}, "x": 0.01},
        margin={"l": 16, "r": 16, "t": 62, "b": 20},
        legend={"orientation": "h", "y": 1.08, "x": 0},
        hoverlabel={"bgcolor": CORES["card"], "font_color": CORES["texto"]},
    )
    figura.update_xaxes(gridcolor=CORES["grade"], zeroline=False, title_font={"color": CORES["muted"]})
    figura.update_yaxes(gridcolor=CORES["grade"], zeroline=False, title_font={"color": CORES["muted"]})
    return figura


@st.cache_data
def obter_base_padrao() -> pd.DataFrame:
    return adicionar_metricas(carregar_dados(BASE_DIR / "data" / "ecommerce_2025.csv"))


def carregar_upload(arquivo) -> pd.DataFrame:
    return adicionar_metricas(carregar_dados(arquivo))


st.set_page_config(
    page_title="Laboratório de Demanda, Preço e Margem",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    .stApp {{ background: radial-gradient(circle at 85% 0%, #24133E 0%, {CORES['fundo']} 42%); }}
    [data-testid="stSidebar"] {{ background: #110C24; border-right: 1px solid {CORES['grade']}; }}
    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, #1B1433, #151029);
        border: 1px solid {CORES['grade']};
        border-radius: 16px;
        padding: 16px 18px;
        min-height: 120px;
    }}
    [data-testid="stMetricLabel"] {{ color: {CORES['muted']}; }}
    [data-testid="stMetricValue"] {{ color: {CORES['texto']}; }}
    .hero {{
        border: 1px solid {CORES['grade']};
        background: linear-gradient(120deg, rgba(255,77,141,.16), rgba(138,99,210,.10));
        border-radius: 22px;
        padding: 30px 34px 26px;
        margin-bottom: 22px;
    }}
    .eyebrow {{ color: {CORES['magenta']}; font-weight: 750; letter-spacing: .12em; font-size: .78rem; }}
    .hero h1 {{ color: {CORES['texto']}; font-size: 2.55rem; line-height: 1.05; margin: 9px 0 12px; }}
    .hero p {{ color: {CORES['muted']}; font-size: 1.05rem; max-width: 860px; margin: 0; }}
    .insight {{
        background: #17112C;
        border-left: 4px solid {CORES['ambar']};
        border-radius: 10px;
        padding: 14px 16px;
        color: {CORES['texto']};
        margin: 8px 0;
    }}
    .method {{
        background: #17112C;
        border: 1px solid {CORES['grade']};
        border-radius: 14px;
        padding: 18px;
        height: 100%;
    }}
    div[data-baseweb="tab-list"] {{ gap: 8px; }}
    button[data-baseweb="tab"] {{ background: #17112C; border-radius: 10px; padding: 10px 16px; }}
    .stDownloadButton button, .stButton button {{ border-radius: 10px; border: 1px solid {CORES['violeta']}; }}

/* Interface revisada: contraste, hierarquia e navegação responsiva. */
:root {{ --ui-accent: #A78BFA; --ui-surface: #141E2E; --ui-ink: #F1F5FA; --ui-muted: #B0BED0; --ui-line: #2C3A4F; }}
.stApp {{ background: #0C1220 !important; }}
.stApp .block-container {{ max-width: 1400px; padding-top: 1.2rem; padding-bottom: 3.5rem; }}
[data-testid="stSidebar"] {{ background: #141E2E !important; border-right: 1px solid #2C3A4F !important; }}
.workspace-bar {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; color: #B0BED0; padding: 2px 0 17px; margin-bottom: 6px; border-bottom: 1px solid #2C3A4F; font-size: .78rem; }}
.workspace-bar strong {{ color: #F1F5FA; font-weight: 650; }}
.workspace-source {{ border: 1px solid #2C3A4F; border-radius: 6px; padding: 4px 9px; background: #141E2E; color: #B0BED0; font-size: .72rem; }}
.stApp .hero {{ border: 1px solid #2C3A4F !important; border-left: 4px solid #A78BFA !important; border-radius: 12px !important; padding: 24px 28px !important; background: #141E2E !important; box-shadow: none !important; margin-bottom: 20px !important; }}
.stApp .hero h1 {{ color: #F7FAFF; font-size: clamp(1.65rem, 2.4vw, 2.3rem) !important; line-height: 1.2 !important; letter-spacing: -.035em; max-width: 1000px; margin: 6px 0 10px !important; }}
.stApp .hero p {{ color: #C5D1E0 !important; font-size: .96rem !important; line-height: 1.65 !important; max-width: 940px !important; }}
.stApp .hero .eyebrow, .stApp .hero-kicker {{ color: #A78BFA !important; font-size: .69rem !important; letter-spacing: .11em !important; }}
.stApp h1 {{ font-size: clamp(1.7rem, 2.5vw, 2.4rem); line-height: 1.2; letter-spacing: -.035em; }}
.stApp h2 {{ font-size: 1.4rem; letter-spacing: -.02em; }}
.stApp h3 {{ font-size: 1.13rem; letter-spacing: -.015em; }}
[data-testid="stMetric"] {{ background: #141E2E !important; border: 1px solid #2C3A4F !important; border-top: 2px solid #2C3A4F !important; border-radius: 10px !important; padding: 18px 20px !important; box-shadow: none !important; min-height: 112px; }}
[data-testid="stMetricLabel"] {{ color: #B0BED0 !important; font-size: .81rem !important; }}
[data-testid="stMetricValue"] {{ color: #F1F5FA !important; font-size: 1.75rem !important; font-weight: 700 !important; font-variant-numeric: tabular-nums; }}
[data-testid="stDataFrame"] {{ border: 1px solid #2C3A4F; border-radius: 10px; overflow: hidden; }}
[data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"] {{ border: 1px solid #2C3A4F; border-radius: 12px; padding: 10px; background: #141E2E; }}
.stTabs [data-baseweb="tab-list"] {{ gap: 8px !important; border-bottom: 1px solid #2C3A4F; overflow-x: auto; padding-bottom: 3px; }}
.stTabs [data-baseweb="tab"] {{ background: transparent !important; padding: 9px 12px !important; border-radius: 6px !important; font-size: .87rem; white-space: nowrap; }}
.stTabs [aria-selected="true"] {{ color: #A78BFA !important; border: none !important; background: #141E2E !important; font-weight: 650; }}
.stButton > button, .stDownloadButton > button {{ border-radius: 7px; min-height: 42px; font-weight: 600; }}
.stApp button:focus-visible, .stApp input:focus-visible, .stApp textarea:focus-visible, .stApp a:focus-visible {{ outline: 3px solid #A78BFA; outline-offset: 3px; }}
.stApp .lesson-card, .stApp .schema-card, .stApp .clause-card, .stApp .step {{ box-shadow: none !important; border-radius: 10px !important; }}
@media (max-width: 900px) {{
  .stApp .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
  .stApp .hero {{ padding: 20px !important; }}
  [data-testid="stHorizontalBlock"] {{ flex-wrap: wrap; }}
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{ min-width: min(240px, 100%); flex: 1 1 240px; }}
  [data-testid="stMetricValue"] {{ font-size: 1.5rem !important; }}
}}
@media (prefers-reduced-motion: reduce) {{ .stApp *, .stApp *::before, .stApp *::after {{ scroll-behavior: auto !important; transition: none !important; animation: none !important; }} }}
</style>
<div class="workspace-bar"><strong>Varejo · Análise comercial</strong><span class="workspace-source">Amostra sintética · 2025</span></div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">CIÊNCIA DE DADOS APLICADA AO VAREJO DIGITAL</div>
        <h1>Laboratório de Demanda, Preço e Margem</h1>
        <p>Uma análise reproduzível para investigar o que acompanha o volume vendido, onde o crescimento perde rentabilidade e quais produtos concentram o resultado.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### Base de análise")
arquivo = st.sidebar.file_uploader("Usar outro CSV", type="csv", help="O arquivo deve seguir o dicionário disponível na documentação.")
try:
    dados = carregar_upload(arquivo) if arquivo is not None else obter_base_padrao()
except (ValueError, KeyError, pd.errors.ParserError) as erro:
    st.error(f"Não foi possível usar o arquivo: {erro}")
    st.stop()

st.sidebar.caption("A base padrão é sintética, reproduzível e cobre 2025. Ela foi criada para estudo de portfólio.")
st.sidebar.markdown("### Filtros")
periodo = st.sidebar.date_input(
    "Período",
    value=(dados["semana"].min().date(), dados["semana"].max().date()),
    min_value=dados["semana"].min().date(),
    max_value=dados["semana"].max().date(),
)
categorias = st.sidebar.multiselect("Categorias", sorted(dados["categoria"].unique()), default=sorted(dados["categoria"].unique()))
canais = st.sidebar.multiselect("Canais", sorted(dados["canal"].unique()), default=sorted(dados["canal"].unique()))

if not isinstance(periodo, (tuple, list)) or len(periodo) != 2:
    st.info("Selecione uma data inicial e uma data final.")
    st.stop()

inicio, fim = pd.to_datetime(periodo[0]), pd.to_datetime(periodo[1])
filtro = dados[
    dados["semana"].between(inicio, fim)
    & dados["categoria"].isin(categorias)
    & dados["canal"].isin(canais)
].copy()

if filtro.empty:
    st.warning("Nenhum registro atende aos filtros selecionados.")
    st.stop()

st.caption(f"{numero(len(filtro))} combinações semana, produto e canal no recorte selecionado. Valores financeiros em reais.")

abas = st.tabs([
    "Visão executiva",
    "Demanda e conversão",
    "Rentabilidade",
    "Produtos e curva ABC",
    "Simulador comercial",
    "Metodologia",
])

with abas[0]:
    kpis = calcular_kpis(filtro)
    colunas = st.columns(3) + st.columns(3)
    colunas[0].metric("Receita líquida", moeda(kpis["receita_liquida"]))
    colunas[1].metric("Lucro bruto", moeda(kpis["lucro_bruto"]))
    colunas[2].metric("Contribuição", moeda(kpis["contribuicao"]))
    colunas[3].metric("Unidades líquidas", numero(kpis["unidades_liquidas"]))
    colunas[4].metric("Conversão", percentual(kpis["conversao_pct"]))
    colunas[5].metric("Margem de contribuição", percentual(kpis["margem_contribuicao_pct"]))

    mensal = resumo_mensal(filtro)
    figura_tempo = go.Figure()
    figura_tempo.add_trace(go.Scatter(x=mensal["mes"], y=mensal["receita_liquida"], name="Receita líquida", mode="lines+markers", line={"color": CORES["magenta"], "width": 3}))
    figura_tempo.add_trace(go.Scatter(x=mensal["mes"], y=mensal["contribuicao"], name="Contribuição", mode="lines+markers", line={"color": CORES["ambar"], "width": 3}))
    figura_tempo.update_layout(title="Receita e contribuição por mês")
    figura_tempo.update_yaxes(tickprefix="R$ ", tickformat="~s")
    st.plotly_chart(aplicar_tema(figura_tempo, 430), width="stretch")

    esquerda, direita = st.columns([1.18, 0.82])
    categorias_resumo = resumo_categoria(filtro)
    with esquerda:
        figura_categoria = px.bar(
            categorias_resumo.sort_values("receita_liquida"),
            x="receita_liquida",
            y="categoria",
            orientation="h",
            color="margem_contribuicao_pct",
            color_continuous_scale=[CORES["violeta"], CORES["magenta"], CORES["ambar"]],
            labels={"receita_liquida": "Receita líquida", "categoria": "", "margem_contribuicao_pct": "Margem"},
            title="Receita por categoria e margem de contribuição",
        )
        figura_categoria.update_xaxes(tickprefix="R$ ", tickformat="~s")
        figura_categoria.update_coloraxes(colorbar_tickformat=".0%")
        st.plotly_chart(aplicar_tema(figura_categoria, 440), width="stretch")
    with direita:
        st.markdown("#### Leitura do recorte")
        for insight in principais_insights(filtro):
            st.markdown(f'<div class="insight">{insight}</div>', unsafe_allow_html=True)
        st.caption("As leituras descrevem a base selecionada. Elas não demonstram causalidade.")

with abas[1]:
    st.subheader("O que acompanha o volume líquido vendido")
    st.write("A correlação de Spearman mede se duas variáveis tendem a subir ou cair juntas. Ela não prova que uma variável causa a outra.")
    associacoes = associacoes_volume(filtro)
    associacoes["direcao"] = associacoes["correlacao_spearman"].apply(lambda valor: "Positiva" if valor >= 0 else "Negativa")
    figura_assoc = px.bar(
        associacoes,
        x="correlacao_spearman",
        y="fator",
        orientation="h",
        color="direcao",
        color_discrete_map={"Positiva": CORES["verde"], "Negativa": CORES["magenta"]},
        text=associacoes["correlacao_spearman"].map(lambda valor: f"{valor:.2f}"),
        title="Associação monotônica com unidades líquidas",
        labels={"correlacao_spearman": "Correlação de Spearman", "fator": ""},
    )
    figura_assoc.update_xaxes(range=[-1, 1])
    figura_assoc.update_traces(textposition="outside")
    st.plotly_chart(aplicar_tema(figura_assoc, 470), width="stretch")

    esquerda, direita = st.columns(2)
    with esquerda:
        amostra = filtro.sample(min(1600, len(filtro)), random_state=42)
        figura_preco = px.scatter(
            amostra,
            x="preco_liquido",
            y="unidades_liquidas",
            color="categoria",
            size="visitas",
            opacity=0.58,
            hover_data=["produto", "canal", "desconto_pct"],
            title="Preço líquido e volume por observação",
            labels={"preco_liquido": "Preço líquido", "unidades_liquidas": "Unidades líquidas"},
        )
        figura_preco.update_xaxes(tickprefix="R$ ")
        st.plotly_chart(aplicar_tema(figura_preco, 440), width="stretch")
    with direita:
        descontos = resumo_desconto(filtro)
        figura_desconto = go.Figure()
        figura_desconto.add_trace(go.Bar(x=descontos["faixa_desconto"].astype(str), y=descontos["unidades_liquidas"], name="Unidades", marker_color=CORES["violeta"]))
        figura_desconto.add_trace(go.Scatter(x=descontos["faixa_desconto"].astype(str), y=descontos["margem_contribuicao_pct"], name="Margem", yaxis="y2", mode="lines+markers", line={"color": CORES["ambar"], "width": 3}))
        figura_desconto.update_layout(
            title="Volume e margem por faixa de desconto",
            yaxis2={"overlaying": "y", "side": "right", "tickformat": ".0%", "showgrid": False},
        )
        st.plotly_chart(aplicar_tema(figura_desconto, 440), width="stretch")

with abas[2]:
    st.subheader("Crescer com receita é diferente de crescer com contribuição")
    canais_resumo = resumo_canal(filtro)
    categorias_resumo = resumo_categoria(filtro)
    c1, c2 = st.columns(2)
    with c1:
        figura_canal = px.bar(
            canais_resumo,
            x="canal",
            y=["receita_liquida", "lucro_bruto", "contribuicao"],
            barmode="group",
            color_discrete_sequence=[CORES["violeta"], CORES["magenta"], CORES["ambar"]],
            title="Resultado financeiro por canal",
            labels={"value": "Valor", "variable": "Métrica", "canal": ""},
        )
        figura_canal.update_yaxes(tickprefix="R$ ", tickformat="~s")
        st.plotly_chart(aplicar_tema(figura_canal, 450), width="stretch")
    with c2:
        figura_quadrante = px.scatter(
            categorias_resumo,
            x="receita_liquida",
            y="margem_contribuicao_pct",
            size="receita_liquida",
            color="categoria",
            text="categoria",
            title="Escala e eficiência por categoria",
            labels={"receita_liquida": "Receita líquida", "margem_contribuicao_pct": "Margem de contribuição"},
        )
        figura_quadrante.update_xaxes(tickprefix="R$ ", tickformat="~s")
        figura_quadrante.update_yaxes(tickformat=".0%")
        figura_quadrante.update_traces(textposition="top center")
        st.plotly_chart(aplicar_tema(figura_quadrante, 450), width="stretch")

    descontos = resumo_desconto(filtro).copy()
    st.markdown("#### Desconto, volume e resultado")
    st.dataframe(
        descontos.rename(columns={
            "faixa_desconto": "Faixa de desconto",
            "receita_liquida": "Receita líquida",
            "contribuicao": "Contribuição",
            "unidades_liquidas": "Unidades líquidas",
            "margem_contribuicao_pct": "Margem de contribuição",
            "conversao_pct": "Conversão",
        })[["Faixa de desconto", "Receita líquida", "Contribuição", "Unidades líquidas", "Margem de contribuição", "Conversão"]].style.format({
            "Receita líquida": "R$ {:,.0f}",
            "Contribuição": "R$ {:,.0f}",
            "Unidades líquidas": "{:,.0f}",
            "Margem de contribuição": "{:.1%}",
            "Conversão": "{:.1%}",
        }),
        width="stretch",
        hide_index=True,
    )

with abas[3]:
    produtos = curva_abc(filtro)
    totais_abc = produtos.groupby("classe_abc", as_index=False).agg(produtos=("sku", "count"), receita=("receita_liquida", "sum"))
    colunas = st.columns(3)
    for coluna, classe, cor in zip(colunas, ["A", "B", "C"], [CORES["magenta"], CORES["ambar"], CORES["violeta"]]):
        linha = totais_abc[totais_abc["classe_abc"] == classe]
        qtd = int(linha["produtos"].iloc[0]) if len(linha) else 0
        receita = float(linha["receita"].iloc[0]) if len(linha) else 0.0
        coluna.markdown(f"<div class='method' style='border-top:4px solid {cor}'><b>Classe {classe}</b><br><span style='font-size:1.65rem'>{qtd} produtos</span><br><span style='color:{CORES['muted']}'>{moeda(receita)} em receita</span></div>", unsafe_allow_html=True)

    produtos_grafico = produtos.copy()
    produtos_grafico["ordem"] = range(1, len(produtos_grafico) + 1)
    figura_abc = go.Figure()
    figura_abc.add_trace(go.Bar(x=produtos_grafico["ordem"], y=produtos_grafico["receita_liquida"], name="Receita por produto", marker_color=CORES["violeta"]))
    figura_abc.add_trace(go.Scatter(x=produtos_grafico["ordem"], y=produtos_grafico["participacao_acumulada_pct"], name="Participação acumulada", yaxis="y2", line={"color": CORES["ambar"], "width": 3}))
    figura_abc.add_shape(
        type="line",
        x0=1,
        x1=len(produtos_grafico),
        y0=0.80,
        y1=0.80,
        xref="x",
        yref="y2",
        line={"color": CORES["magenta"], "dash": "dot", "width": 2},
    )
    figura_abc.update_layout(
        title="Curva ABC de produtos por receita líquida",
        xaxis_title="Produtos ordenados por receita",
        yaxis_title="Receita líquida",
        yaxis2={"overlaying": "y", "side": "right", "tickformat": ".0%", "range": [0, 1.05], "showgrid": False},
    )
    figura_abc.update_yaxes(tickprefix="R$ ", tickformat="~s")
    st.plotly_chart(aplicar_tema(figura_abc, 460), width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        ranking_ruptura = produtos.sort_values("taxa_ruptura_pct", ascending=False).head(10)
        figura_ruptura = px.bar(ranking_ruptura.sort_values("taxa_ruptura_pct"), x="taxa_ruptura_pct", y="produto", orientation="h", color_discrete_sequence=[CORES["magenta"]], title="Produtos com maior frequência de ruptura", labels={"taxa_ruptura_pct": "Frequência de ruptura", "produto": ""})
        figura_ruptura.update_xaxes(tickformat=".0%")
        st.plotly_chart(aplicar_tema(figura_ruptura, 430), width="stretch")
    with col2:
        ranking_devolucao = produtos.sort_values("taxa_devolucao_pct", ascending=False).head(10)
        figura_devolucao = px.bar(ranking_devolucao.sort_values("taxa_devolucao_pct"), x="taxa_devolucao_pct", y="produto", orientation="h", color_discrete_sequence=[CORES["ambar"]], title="Produtos com maior taxa de devolução", labels={"taxa_devolucao_pct": "Taxa de devolução", "produto": ""})
        figura_devolucao.update_xaxes(tickformat=".0%")
        st.plotly_chart(aplicar_tema(figura_devolucao, 430), width="stretch")

    st.download_button(
        "Baixar análise ABC em CSV",
        produtos.to_csv(index=False).encode("utf-8"),
        file_name="curva_abc_produtos.csv",
        mime="text/csv",
    )

with abas[4]:
    st.subheader("Simulador de cenário comercial")
    st.warning("Este módulo é uma simulação de planejamento. Ele não é um modelo preditivo e não estima o efeito causal de preço ou mídia.")
    f1, f2 = st.columns(2)
    with f1:
        categoria_sim = st.selectbox("Categoria", sorted(filtro["categoria"].unique()))
        canais_validos = sorted(filtro.loc[filtro["categoria"] == categoria_sim, "canal"].unique())
        canal_sim = st.selectbox("Canal", canais_validos)
    with f2:
        elasticidade = st.slider("Elasticidade-preço assumida", min_value=-3.0, max_value=-0.5, value=-1.5, step=0.1, help="Valor de cenário: quanto a demanda reage proporcionalmente à mudança de preço.")

    c1, c2, c3 = st.columns(3)
    ajuste_preco = c1.slider("Ajuste no preço de lista", -15, 15, 0, 1, format="%d%%")
    desconto = c2.slider("Desconto comercial", 0, 30, 10, 1, format="%d%%")
    trafego = c3.slider("Variação de tráfego", -30, 50, 0, 5, format="%d%%")
    base_sim = filtro[(filtro["categoria"] == categoria_sim) & (filtro["canal"] == canal_sim)]
    cenario = simular_cenario(base_sim, ajuste_preco, desconto, trafego, elasticidade)

    st.markdown("#### Comparação semanal")
    metricas = st.columns(4)
    metricas[0].metric("Preço líquido", moeda(cenario["preco_liquido_cenario"]), delta_pct(cenario["preco_liquido_cenario"], cenario["preco_liquido_base"]))
    metricas[1].metric("Unidades", numero(cenario["unidades_cenario"]), delta_pct(cenario["unidades_cenario"], cenario["unidades_base"]))
    metricas[2].metric("Receita", moeda(cenario["receita_cenario"]), delta_pct(cenario["receita_cenario"], cenario["receita_base"]))
    metricas[3].metric("Contribuição", moeda(cenario["contribuicao_cenario"]), delta_pct(cenario["contribuicao_cenario"], cenario["contribuicao_base"]))
    st.caption(f"Margem de contribuição estimada no cenário: {percentual(cenario['margem_contribuicao_cenario'])}. Compare cenários e valide as hipóteses antes de qualquer decisão real.")

with abas[5]:
    st.subheader("Como este laboratório foi construído")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='method'><b>1. Dados</b><br>Base semanal sintética com 48 produtos, 8 categorias, 3 canais e semente fixa. As relações foram programadas e documentadas.</div>", unsafe_allow_html=True)
    c2.markdown("<div class='method'><b>2. Métricas</b><br>Receita líquida, custos, lucro bruto, contribuição, conversão, devolução, ROAS e ruptura são calculados por funções testáveis.</div>", unsafe_allow_html=True)
    c3.markdown("<div class='method'><b>3. Decisão</b><br>As páginas conectam demanda, rentabilidade, portfólio e cenários sem apresentar associação como causalidade.</div>", unsafe_allow_html=True)
    st.markdown("#### Fórmulas principais")
    st.code(
        """preço líquido = preço de lista × (1 - desconto)
receita líquida = unidades líquidas × preço líquido
lucro bruto = receita líquida - custo do produto - taxa do canal
contribuição = lucro bruto - investimento em mídia
conversão = pedidos ÷ visitas""",
        language="text",
    )
    st.markdown("#### Limitações")
    st.write(
        "Os dados não representam uma empresa real. As correlações refletem relações construídas na simulação e podem mudar com os filtros. "
        "O simulador usa elasticidade informada pelo usuário, não um parâmetro estimado. Não foram considerados impostos, frete, cancelamentos, estoque futuro ou incrementabilidade da mídia."
    )
    st.markdown("#### Dados do recorte")
    st.dataframe(filtro.sort_values(["semana", "produto", "canal"], ascending=[False, True, True]), width="stretch", hide_index=True)
    st.download_button("Baixar recorte em CSV", filtro.to_csv(index=False).encode("utf-8"), file_name="recorte_ecommerce.csv", mime="text/csv")

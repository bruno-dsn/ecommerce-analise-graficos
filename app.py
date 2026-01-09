# app.py
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.figure_factory as ff

# 1) Ler a base
df = pd.read_csv('ecommerce_estatistica.csv')

# 2) Garantir tipos numéricos
num_cols = [
    'Nota', 'N_Avaliações', 'Desconto', 'Preço',
    'Nota_MinMax', 'N_Avaliações_MinMax', 'Desconto_MinMax', 'Preço_MinMax',
    'Marca_Cod', 'Material_Cod', 'Temporada_Cod',
    'Qtd_Vendidos', 'Qtd_Vendidos_Cod', 'Marca_Freq', 'Material_Freq'
]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# Fallbacks de nomes frequentes
col_preco = 'Preço' if 'Preço' in df.columns else ('Preco' if 'Preco' in df.columns else 'Preço_MinMax')
col_av = 'N_Avaliações' if 'N_Avaliações' in df.columns else ('N_Avaliacoes' if 'N_Avaliacoes' in df.columns else 'N_Avaliações_MinMax')
col_desc = 'Desconto' if 'Desconto' in df.columns else 'Desconto_MinMax'
col_qtd = 'Qtd_Vendidos_Cod' if 'Qtd_Vendidos_Cod' in df.columns else ('Qtd_Vendidos' if 'Qtd_Vendidos' in df.columns else None)

# 3) App
app = Dash(__name__)
app.title = "Ecommerce dashboard"

# Listas dinâmicas para controles
num_options = [c for c in df.columns if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
cat_options = [c for c in df.columns if df[c].dtype == 'object']

# Layout
app.layout = html.Div([
    html.H1("Ecommerce dashboard"),
    html.P("Explore os dados e gráficos de forma interativa."),
    dcc.Tabs([
        dcc.Tab(label="Resumo", children=[
            html.Div([
                html.Div([
                    html.H3("Dimensão do dataset"),
                    html.P(f"{df.shape[0]} linhas, {df.shape[1]} colunas")
                ]),
                html.Div([
                    html.H3("Colunas numéricas"),
                    html.P(", ".join(num_options))
                ]),
                html.Div([
                    html.H3("Colunas categóricas"),
                    html.P(", ".join(cat_options))
                ]),
            ], style={"columnCount": 2})
        ]),
        dcc.Tab(label="Histograma (Preço)", children=[
            html.Div([
                html.Label("Escolha a coluna numérica:"),
                dcc.Dropdown(
                    id="hist-col",
                    options=[{"label": c, "value": c} for c in num_options],
                    value=col_preco,
                    clearable=False
                ),
                dcc.Slider(id="hist-bins", min=10, max=80, step=5, value=30),
                html.Br(),
                dcc.Graph(id="hist-graph")
            ])
        ]),
        dcc.Tab(label="Dispersão (Preço vs Avaliações)", children=[
            html.Div([
                html.Label("Eixo X (numérico):"),
                dcc.Dropdown(
                    id="scatter-x",
                    options=[{"label": c, "value": c} for c in num_options],
                    value=col_preco,
                    clearable=False
                ),
                html.Label("Eixo Y (numérico):"),
                dcc.Dropdown(
                    id="scatter-y",
                    options=[{"label": c, "value": c} for c in num_options],
                    value=col_av,
                    clearable=False
                ),
                html.Label("Cor por categoria (opcional):"),
                dcc.Dropdown(
                    id="scatter-color",
                    options=[{"label": c, "value": c} for c in cat_options],
                    value=("Marca" if "Marca" in df.columns else None),
                    clearable=True
                ),
                dcc.Graph(id="scatter-graph")
            ])
        ]),
        dcc.Tab(label="Mapa de calor (correlações)", children=[
            html.Div([
                dcc.Graph(id="heatmap-graph")
            ])
        ]),
        dcc.Tab(label="Barra (Top marcas)", children=[
            html.Div([
                html.Label("Coluna categórica:"),
                dcc.Dropdown(
                    id="bar-cat",
                    options=[{"label": c, "value": c} for c in cat_options],
                    value=("Marca" if "Marca" in df.columns else (cat_options[0] if cat_options else None)),
                    clearable=False
                ),
                html.Label("Top N:"),
                dcc.Slider(id="bar-topn", min=5, max=25, step=5, value=15),
                dcc.Graph(id="bar-graph")
            ])
        ]),
        dcc.Tab(label="Pizza (Materiais)", children=[
            html.Div([
                html.Label("Coluna categórica:"),
                dcc.Dropdown(
                    id="pie-cat",
                    options=[{"label": c, "value": c} for c in cat_options],
                    value=("Material" if "Material" in df.columns else (cat_options[0] if cat_options else None)),
                    clearable=False
                ),
                html.Label("Top N:"),
                dcc.Slider(id="pie-topn", min=5, max=12, step=1, value=8),
                dcc.Graph(id="pie-graph")
            ])
        ]),
        dcc.Tab(label="Densidade (Desconto)", children=[
            html.Div([
                html.Label("Coluna numérica:"),
                dcc.Dropdown(
                    id="kde-col",
                    options=[{"label": c, "value": c} for c in num_options],
                    value=col_desc,
                    clearable=False
                ),
                dcc.Graph(id="kde-graph")
            ])
        ]),
        dcc.Tab(label="Regressão (Preço vs Vendas)", children=[
            html.Div([
                html.Label("Eixo X (numérico):"),
                dcc.Dropdown(
                    id="reg-x",
                    options=[{"label": c, "value": c} for c in num_options],
                    value=col_preco,
                    clearable=False
                ),
                html.Label("Eixo Y (numérico):"),
                dcc.Dropdown(
                    id="reg-y",
                    options=[{"label": c, "value": c} for c in num_options],
                    value=(col_qtd if col_qtd else num_options[0]),
                    clearable=False
                ),
                dcc.Graph(id="reg-graph")
            ])
        ]),
    ])
])

# Callbacks

@app.callback(Output("hist-graph", "figure"),
              Input("hist-col", "value"), Input("hist-bins", "value"))
def update_hist(col, bins):
    data = df[col].dropna()
    fig = px.histogram(data, x=data, nbins=bins, title=f"Distribuição de {col}")
    fig.update_layout(xaxis_title=col, yaxis_title="Contagem")
    return fig

@app.callback(Output("scatter-graph", "figure"),
              Input("scatter-x", "value"), Input("scatter-y", "value"), Input("scatter-color", "value"))
def update_scatter(x, y, color):
    fig = px.scatter(df, x=x, y=y, color=color,
                     opacity=0.7, title=f"Dispersão: {x} vs {y}")
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    return fig

@app.callback(Output("heatmap-graph", "figure"), Input("heatmap-graph", "id"))
def update_heatmap(_):
    corr = df.select_dtypes(include=[np.number]).corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu", title="Mapa de calor de correlações")
    return fig

@app.callback(Output("bar-graph", "figure"),
              Input("bar-cat", "value"), Input("bar-topn", "value"))
def update_bar(cat_col, topn):
    vc = df[cat_col].value_counts().head(topn)
    fig = px.bar(vc[::-1], x=vc.values[::-1], y=vc.index[::-1], orientation='h',
                 title=f"Frequência de {cat_col} (Top {topn})")
    fig.update_layout(xaxis_title="Contagem", yaxis_title=cat_col)
    return fig

@app.callback(Output("pie-graph", "figure"),
              Input("pie-cat", "value"), Input("pie-topn", "value"))
def update_pie(cat_col, topn):
    vc = df[cat_col].value_counts().head(topn)
    fig = px.pie(values=vc.values, names=vc.index, title=f"Distribuição de {cat_col} (Top {topn})", hole=0.0)
    return fig

@app.callback(Output("kde-graph", "figure"),
              Input("kde-col", "value"))
def update_kde(col):
    data = df[col].dropna()
    fig = ff.create_distplot([data.values], group_labels=[col], show_hist=False, show_rug=False)
    fig.update_layout(title=f"Densidade de {col}", xaxis_title=col, yaxis_title="Densidade")
    return fig

@app.callback(Output("reg-graph", "figure"),
              Input("reg-x", "value"), Input("reg-y", "value"))
def update_reg(x, y):
    fig = px.scatter(df, x=x, y=y, opacity=0.6)
    # Adiciona linha de regressão usando trendline do plotly express (OLS)
    try:
        fig_trend = px.scatter(df, x=x, y=y, trendline="ols")
        # Mescla a linha de regressão
        for d in fig_trend.data:
            if d.mode == "lines":
                fig.add_trace(d)
    except Exception:
        pass
    fig.update_layout(title=f"Regressão: {x} vs {y}", xaxis_title=x, yaxis_title=y)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)

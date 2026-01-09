import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Lê o arquivo CSV
df = pd.read_csv("ecommerce_estatistica.csv")

# Cria a aplicação Dash
app = dash.Dash(__name__)

# Gráficos básicos
fig_hist = px.histogram(df, x="Preço", nbins=30, title="Histograma de Preços")

fig_disp = px.scatter(df, x="Preço", y="N_Avaliações", title="Dispersão: Preço vs Avaliações")

fig_heat = px.imshow(
    df.select_dtypes(include="number").corr(),
    text_auto=True,
    title="Mapa de Calor das Correlações"
)

fig_bar = px.bar(
    df["Marca"].value_counts().head(10),
    title="Top 10 Marcas"
)

fig_pie = px.pie(
    names=df["Material"].value_counts().head(5).index,
    values=df["Material"].value_counts().head(5).values,
    title="Distribuição de Materiais"
)

fig_kde = px.histogram(df, x="Desconto", nbins=30, marginal="box", title="Distribuição de Descontos")

# Gráfico de regressão (agora funciona porque você instalou statsmodels)
fig_reg = px.scatter(
    df, x="Preço", y="Qtd_Vendidos_Cod",
    trendline="ols",
    title="Regressão: Preço vs Vendas"
)

# Layout da página
app.layout = html.Div([
    html.H1("Dashboard Ecommerce"),
    dcc.Graph(figure=fig_hist),
    dcc.Graph(figure=fig_disp),
    dcc.Graph(figure=fig_heat),
    dcc.Graph(figure=fig_bar),
    dcc.Graph(figure=fig_pie),
    dcc.Graph(figure=fig_kde),
    dcc.Graph(figure=fig_reg),
])

# Executa o servidor
if __name__ == "__main__":
    app.run(debug=False)



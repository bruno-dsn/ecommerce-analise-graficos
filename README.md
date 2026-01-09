# ecommerce-analise-graficos

# Análise gráfica de dados de ecommerce

Este repositório contém um notebook com leitura do arquivo `ecommerce_estatistica.csv`, análise descritiva e gráficos solicitados:
- Histograma
- Dispersão
- Mapa de calor (correlações)
- Barra (frequência de categorias)
- Pizza (distribuição de materiais)
- Densidade (kde)
- Regressão

## Objetivos
- Explorar padrões de preço, avaliações, desconto e vendas.
- Identificar relações relevantes para estratégias de catálogo e precificação.

## Como rodar
1. Abra no Google Colab ou Jupyter Notebook.
2. Faça upload do `ecommerce_estatistica.csv` na mesma pasta do notebook.
3. Execute as células na ordem.

## Principais colunas
- Numéricas: Preço, Nota, N_Avaliações, Desconto, Qtd_Vendidos_Cod, e versões MinMax.
- Categóricas: Marca, Material, Temporada.

## Bibliotecas
- pandas, numpy, matplotlib, seaborn

## Insights esperados
- Distribuições de preço e desconto
- Correlações com `Qtd_Vendidos_Cod`
- Marcas e materiais predominantes
- Relação entre preço e vendas

## Estrutura
- `ecommerce-analise-graficos.ipynb`: Notebook principal
- `ecommerce_estatistica.csv`: Base de dados usada

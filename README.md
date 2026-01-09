# 📊 Dashboard de Ecommerce

Este projeto mostra alguns gráficos simples usando **Dash** e os dados do arquivo `ecommerce_estatistica.csv`.

## 🚀 Objetivo
- Ler os dados de ecommerce.
- Mostrar gráficos básicos sem precisar rodar código no Python manualmente.
- Facilitar a visualização para o usuário final.

## 📂 Estrutura
- `ecommerce-analise-graficos.ipynb` → Notebook com análises anteriores.
- `ecommerce_estatistica.csv` → Base de dados usada.
- `app.py` → Aplicação Dash simples.
- `README.md` → Explicação do projeto.

## 📊 Gráficos exibidos
1. Histograma de preços  
2. Dispersão: preço vs avaliações  
3. Mapa de calor das correlações  
4. Barra: top marcas  
5. Pizza: distribuição de materiais  
6. Densidade de descontos  
7. Regressão: preço vs vendas  

## Como executar
1. Instale as bibliotecas necessárias:
   ```bash
   pip install dash pandas plotly

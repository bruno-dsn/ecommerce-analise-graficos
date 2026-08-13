# Dados e metodologia

## Objetivo

O projeto investiga relações entre demanda, preço, tráfego, conversão e rentabilidade em um e-commerce. Como não havia uma base pública com todas essas variáveis na mesma granularidade, foi criada uma base sintética reproduzível.

## Unidade de análise

Cada linha representa uma combinação de semana, produto e canal. A base cobre as 52 semanas de 2025, 48 produtos, 8 categorias e 3 canais, totalizando 7.488 observações.

## Como os dados foram gerados

O gerador usa `numpy.random.default_rng` com semente 42. Configurações explícitas definem preço, custo, tráfego, conversão, devolução e elasticidade por categoria. Configurações adicionais representam diferenças entre Site, Aplicativo e Marketplace.

O fluxo simplificado é:

1. Criar o catálogo e atributos fixos dos produtos.
2. Aplicar sazonalidade semanal, incluindo maior demanda em novembro e dezembro.
3. Sortear desconto, preço, mídia, avaliação e prazo de entrega.
4. Calcular a conversão esperada a partir de preço, avaliação, prazo e canal.
5. Sortear pedidos e demanda em unidades.
6. Limitar vendas pelo estoque disponível.
7. Sortear devoluções de acordo com a categoria.
8. Calcular receita, custos, lucro e contribuição.

## Relações programadas

As relações abaixo foram incluídas intencionalmente para que o laboratório tenha um comportamento comercial coerente:

- mais visitas criam mais oportunidades de pedido;
- preço líquido menor tende a elevar conversão;
- avaliação melhor tende a apoiar conversão;
- prazo de entrega maior tende a reduzir conversão;
- Marketplace possui maior taxa de canal;
- Moda possui maior propensão a devolução;
- períodos promocionais recebem maior tráfego e desconto;
- ruptura limita as unidades vendidas.

## Associação de Spearman

A correlação de Spearman foi usada porque mede se duas variáveis tendem a variar na mesma direção, mesmo quando a relação não é linear.

O cálculo é feito sobre os postos das variáveis:

```text
rho = correlação de Pearson entre os postos de X e Y
```

Um valor próximo de 1 indica associação positiva forte. Um valor próximo de menos 1 indica associação negativa forte. Um valor próximo de zero indica pouca associação monotônica.

## Métricas financeiras

```text
preço líquido = preço de lista × (1 - desconto)
unidades líquidas = unidades vendidas - devoluções
receita líquida = unidades líquidas × preço líquido
custo do produto = unidades líquidas × custo unitário
custo do canal = receita líquida × taxa do canal
lucro bruto = receita líquida - custo do produto - custo do canal
contribuição = lucro bruto - investimento em mídia
```

## Curva ABC

Os produtos são ordenados pela receita líquida. A participação acumulada determina a classe:

- A: até 80% da receita acumulada;
- B: de 80% até 95%;
- C: parcela restante.

## Simulador

O simulador parte da média semanal do recorte e aplica quatro hipóteses informadas pelo usuário: ajuste do preço de lista, desconto, variação de tráfego e elasticidade.

```text
unidades do cenário = unidades base × razão de preço ^ elasticidade × fator de tráfego
```

O cálculo é um cenário de planejamento. Não é previsão, recomendação automática nem estimativa causal.

## Reprodutibilidade

Para recriar a base:

```bash
python scripts/gerar_dados.py
```

Com a mesma versão das bibliotecas e a mesma semente, a base gerada é determinística.

## Limitações

- Dados sintéticos não substituem validação com dados reais.
- As relações refletem as regras do gerador.
- Correlação não prova causa.
- O simulador usa elasticidade assumida.
- Impostos, frete, cancelamentos e incrementabilidade de mídia não foram modelados.
- As métricas são adequadas ao objetivo didático, não a uma operação real completa.


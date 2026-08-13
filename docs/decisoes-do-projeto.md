# Decisões do projeto

## Por que este problema

Painéis de e-commerce frequentemente param em receita e pedidos. O projeto foi desenhado para avançar uma etapa e mostrar que volume, margem e contribuição podem apontar para decisões diferentes.

## Perguntas definidas antes do código

1. Quais fatores acompanham o volume líquido vendido?
2. Quais categorias combinam escala e margem?
3. Qual canal transforma receita em contribuição com mais eficiência?
4. Descontos maiores aumentam volume sem destruir resultado?
5. Quais produtos concentram receita e quais apresentam risco operacional?
6. Como comparar hipóteses comerciais sem chamar cenário de previsão?

## Escolha da granularidade

Uma base por pedido não mostraria com clareza visitas, conversão e estoque. Por isso, a unidade escolhida foi semana, produto e canal. Essa granularidade permite conectar o funil comercial ao resultado financeiro.

## Separação entre lucro e contribuição

O projeto calcula lucro bruto após produto e taxa do canal. Em seguida, desconta mídia para chegar à contribuição. Essa separação torna explicável a diferença entre Marketplace, Site e Aplicativo.

## Escolha da correlação

Spearman foi escolhido porque preço, conversão e volume não precisam manter uma relação linear. A medida é simples de explicar e adequada a uma análise exploratória.

## Curva ABC com contexto operacional

A classificação ABC sozinha indica concentração. O projeto adiciona ruptura e devolução para mostrar que um produto importante também pode exigir atenção operacional.

## Simulador separado da análise

O simulador aparece em uma aba própria e recebe um aviso explícito. O usuário informa a elasticidade, portanto o resultado não é tratado como parâmetro estimado ou recomendação.

## O que eu faria com dados reais

1. Validaria qualidade, duplicidade, cancelamentos e regras contábeis.
2. Separaria preço observado de promoções direcionadas.
3. Estimaria elasticidade com experimentos ou métodos causais adequados.
4. Mediria incrementabilidade da mídia.
5. Incluiria frete, imposto, comissão, subsídio e custo de devolução.
6. Criaria monitoramento de estabilidade e atualização periódica.


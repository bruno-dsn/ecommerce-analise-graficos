# Dicionário de dados

| Coluna | Tipo | Significado |
|---|---|---|
| `semana` | data | Segunda-feira de referência da observação semanal |
| `sku` | texto | Código único do produto |
| `produto` | texto | Nome comercial fictício |
| `categoria` | texto | Categoria do catálogo |
| `canal` | texto | Site, Aplicativo ou Marketplace |
| `preco_lista` | decimal | Preço antes do desconto |
| `desconto_pct` | inteiro | Percentual de desconto aplicado |
| `custo_unitario` | decimal | Custo unitário do produto |
| `visitas` | inteiro | Visitas atribuídas à combinação produto e canal |
| `pedidos` | inteiro | Pedidos realizados |
| `unidades_vendidas` | inteiro | Unidades entregues antes das devoluções |
| `unidades_devolvidas` | inteiro | Unidades devolvidas |
| `investimento_midia` | decimal | Investimento semanal em mídia |
| `avaliacao_media` | decimal | Nota média do produto entre 1 e 5 |
| `prazo_entrega_dias` | decimal | Prazo médio de entrega em dias |
| `estoque_inicial` | inteiro | Unidades disponíveis na semana |

## Colunas calculadas na aplicação

| Coluna | Significado |
|---|---|
| `preco_liquido` | Preço após desconto |
| `unidades_liquidas` | Vendas menos devoluções |
| `receita_liquida` | Unidades líquidas multiplicadas pelo preço líquido |
| `custo_produto` | Unidades líquidas multiplicadas pelo custo unitário |
| `taxa_canal_pct` | Percentual cobrado pelo canal |
| `custo_canal` | Receita líquida multiplicada pela taxa do canal |
| `lucro_bruto` | Receita menos custo de produto e canal |
| `contribuicao` | Lucro bruto menos mídia |
| `margem_bruta_pct` | Lucro bruto dividido pela receita |
| `margem_contribuicao_pct` | Contribuição dividida pela receita |
| `conversao_pct` | Pedidos divididos por visitas |
| `taxa_devolucao_pct` | Devoluções divididas por unidades vendidas |
| `ruptura_estoque` | Indica venda igual ao estoque disponível |
| `roas` | Receita dividida pelo investimento em mídia |


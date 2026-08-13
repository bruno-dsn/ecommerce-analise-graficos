from __future__ import annotations

import numpy as np
import pandas as pd

from src.data import CANAIS, validar_colunas


def adicionar_metricas(dados: pd.DataFrame) -> pd.DataFrame:
    validar_colunas(dados)
    resultado = dados.copy()
    resultado["semana"] = pd.to_datetime(resultado["semana"])
    resultado["preco_liquido"] = resultado["preco_lista"] * (1 - resultado["desconto_pct"] / 100)
    resultado["unidades_liquidas"] = resultado["unidades_vendidas"] - resultado["unidades_devolvidas"]
    resultado["receita_liquida"] = resultado["unidades_liquidas"] * resultado["preco_liquido"]
    resultado["custo_produto"] = resultado["unidades_liquidas"] * resultado["custo_unitario"]
    resultado["taxa_canal_pct"] = resultado["canal"].map({canal: cfg["taxa_pct"] for canal, cfg in CANAIS.items()})
    resultado["custo_canal"] = resultado["receita_liquida"] * resultado["taxa_canal_pct"]
    resultado["lucro_bruto"] = resultado["receita_liquida"] - resultado["custo_produto"] - resultado["custo_canal"]
    resultado["contribuicao"] = resultado["lucro_bruto"] - resultado["investimento_midia"]
    resultado["margem_bruta_pct"] = np.where(
        resultado["receita_liquida"] > 0,
        resultado["lucro_bruto"] / resultado["receita_liquida"],
        0.0,
    )
    resultado["margem_contribuicao_pct"] = np.where(
        resultado["receita_liquida"] > 0,
        resultado["contribuicao"] / resultado["receita_liquida"],
        0.0,
    )
    resultado["conversao_pct"] = np.where(resultado["visitas"] > 0, resultado["pedidos"] / resultado["visitas"], 0.0)
    resultado["taxa_devolucao_pct"] = np.where(
        resultado["unidades_vendidas"] > 0,
        resultado["unidades_devolvidas"] / resultado["unidades_vendidas"],
        0.0,
    )
    resultado["ruptura_estoque"] = resultado["unidades_vendidas"] >= resultado["estoque_inicial"]
    resultado["roas"] = np.where(
        resultado["investimento_midia"] > 0,
        resultado["receita_liquida"] / resultado["investimento_midia"],
        0.0,
    )
    return resultado


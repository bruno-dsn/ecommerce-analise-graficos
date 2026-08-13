from __future__ import annotations

import pandas as pd


def simular_cenario(
    dados: pd.DataFrame,
    ajuste_preco_pct: float,
    desconto_pct: float,
    variacao_trafego_pct: float,
    elasticidade: float,
) -> dict[str, float]:
    """Compara um cenário hipotético com a média semanal observada no recorte."""
    semanas = max(int(dados["semana"].nunique()), 1)
    unidades_base = float(dados["unidades_liquidas"].sum()) / semanas
    receita_base = float(dados["receita_liquida"].sum()) / semanas
    contribuicao_base = float(dados["contribuicao"].sum()) / semanas
    preco_lista_base = float((dados["preco_lista"] * dados["unidades_liquidas"]).sum() / max(dados["unidades_liquidas"].sum(), 1))
    preco_liquido_base = receita_base / max(unidades_base, 1)
    custo_unitario = float(dados["custo_produto"].sum() / max(dados["unidades_liquidas"].sum(), 1))
    taxa_canal = float(dados["custo_canal"].sum() / max(dados["receita_liquida"].sum(), 1))
    midia_base = float(dados["investimento_midia"].sum()) / semanas

    novo_preco_lista = preco_lista_base * (1 + ajuste_preco_pct / 100)
    novo_preco_liquido = novo_preco_lista * (1 - desconto_pct / 100)
    razao_preco = max(novo_preco_liquido / max(preco_liquido_base, 0.01), 0.1)
    fator_trafego = max(1 + variacao_trafego_pct / 100, 0.1)
    unidades_cenario = unidades_base * (razao_preco ** elasticidade) * fator_trafego
    receita_cenario = unidades_cenario * novo_preco_liquido
    custo_cenario = unidades_cenario * custo_unitario
    custo_canal_cenario = receita_cenario * taxa_canal
    midia_cenario = midia_base * (1 + max(variacao_trafego_pct, 0) / 100 * 0.65)
    contribuicao_cenario = receita_cenario - custo_cenario - custo_canal_cenario - midia_cenario

    return {
        "unidades_base": unidades_base,
        "receita_base": receita_base,
        "contribuicao_base": contribuicao_base,
        "preco_liquido_base": preco_liquido_base,
        "unidades_cenario": unidades_cenario,
        "receita_cenario": receita_cenario,
        "contribuicao_cenario": contribuicao_cenario,
        "preco_liquido_cenario": novo_preco_liquido,
        "margem_contribuicao_cenario": contribuicao_cenario / receita_cenario if receita_cenario else 0.0,
    }


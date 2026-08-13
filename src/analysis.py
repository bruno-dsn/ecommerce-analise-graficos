from __future__ import annotations

import numpy as np
import pandas as pd


def calcular_kpis(dados: pd.DataFrame) -> dict[str, float]:
    receita = float(dados["receita_liquida"].sum())
    lucro = float(dados["lucro_bruto"].sum())
    contribuicao = float(dados["contribuicao"].sum())
    pedidos = int(dados["pedidos"].sum())
    unidades = int(dados["unidades_liquidas"].sum())
    visitas = int(dados["visitas"].sum())
    vendidas = int(dados["unidades_vendidas"].sum())
    devolvidas = int(dados["unidades_devolvidas"].sum())
    return {
        "receita_liquida": receita,
        "lucro_bruto": lucro,
        "contribuicao": contribuicao,
        "pedidos": pedidos,
        "unidades_liquidas": unidades,
        "ticket_medio": receita / pedidos if pedidos else 0.0,
        "margem_bruta_pct": lucro / receita if receita else 0.0,
        "margem_contribuicao_pct": contribuicao / receita if receita else 0.0,
        "conversao_pct": pedidos / visitas if visitas else 0.0,
        "taxa_devolucao_pct": devolvidas / vendidas if vendidas else 0.0,
    }


def resumo_mensal(dados: pd.DataFrame) -> pd.DataFrame:
    copia = dados.copy()
    copia["mes"] = copia["semana"].dt.to_period("M").dt.to_timestamp()
    return copia.groupby("mes", as_index=False).agg(
        receita_liquida=("receita_liquida", "sum"),
        lucro_bruto=("lucro_bruto", "sum"),
        contribuicao=("contribuicao", "sum"),
        unidades_liquidas=("unidades_liquidas", "sum"),
    )


def resumo_categoria(dados: pd.DataFrame) -> pd.DataFrame:
    resumo = dados.groupby("categoria", as_index=False).agg(
        receita_liquida=("receita_liquida", "sum"),
        lucro_bruto=("lucro_bruto", "sum"),
        contribuicao=("contribuicao", "sum"),
        visitas=("visitas", "sum"),
        pedidos=("pedidos", "sum"),
        unidades_vendidas=("unidades_vendidas", "sum"),
        unidades_devolvidas=("unidades_devolvidas", "sum"),
    )
    resumo["margem_bruta_pct"] = resumo["lucro_bruto"] / resumo["receita_liquida"]
    resumo["margem_contribuicao_pct"] = resumo["contribuicao"] / resumo["receita_liquida"]
    resumo["conversao_pct"] = resumo["pedidos"] / resumo["visitas"]
    resumo["taxa_devolucao_pct"] = resumo["unidades_devolvidas"] / resumo["unidades_vendidas"].replace(0, np.nan)
    return resumo.sort_values("receita_liquida", ascending=False).reset_index(drop=True)


def resumo_canal(dados: pd.DataFrame) -> pd.DataFrame:
    resumo = dados.groupby("canal", as_index=False).agg(
        receita_liquida=("receita_liquida", "sum"),
        lucro_bruto=("lucro_bruto", "sum"),
        contribuicao=("contribuicao", "sum"),
        visitas=("visitas", "sum"),
        pedidos=("pedidos", "sum"),
        investimento_midia=("investimento_midia", "sum"),
    )
    resumo["margem_bruta_pct"] = resumo["lucro_bruto"] / resumo["receita_liquida"]
    resumo["margem_contribuicao_pct"] = resumo["contribuicao"] / resumo["receita_liquida"]
    resumo["conversao_pct"] = resumo["pedidos"] / resumo["visitas"]
    resumo["roas"] = resumo["receita_liquida"] / resumo["investimento_midia"]
    return resumo.sort_values("receita_liquida", ascending=False).reset_index(drop=True)


def _spearman(serie_x: pd.Series, serie_y: pd.Series) -> float:
    return float(serie_x.rank(method="average").corr(serie_y.rank(method="average")))


def associacoes_volume(dados: pd.DataFrame) -> pd.DataFrame:
    variaveis = {
        "Visitas": "visitas",
        "Conversão": "conversao_pct",
        "Desconto": "desconto_pct",
        "Investimento em mídia": "investimento_midia",
        "Avaliação": "avaliacao_media",
        "Preço líquido": "preco_liquido",
        "Prazo de entrega": "prazo_entrega_dias",
    }
    linhas = [
        {"fator": rotulo, "correlacao_spearman": _spearman(dados[coluna], dados["unidades_liquidas"])}
        for rotulo, coluna in variaveis.items()
    ]
    resultado = pd.DataFrame(linhas)
    resultado["forca"] = resultado["correlacao_spearman"].abs()
    return resultado.sort_values("forca", ascending=True).reset_index(drop=True)


def resumo_desconto(dados: pd.DataFrame) -> pd.DataFrame:
    copia = dados.copy()
    copia["faixa_desconto"] = pd.cut(
        copia["desconto_pct"],
        bins=[-0.1, 4.9, 9.9, 14.9, 19.9, 100],
        labels=["Sem desconto", "5%", "10%", "15%", "20% ou mais"],
    )
    resumo = copia.groupby("faixa_desconto", observed=False, as_index=False).agg(
        receita_liquida=("receita_liquida", "sum"),
        lucro_bruto=("lucro_bruto", "sum"),
        contribuicao=("contribuicao", "sum"),
        visitas=("visitas", "sum"),
        pedidos=("pedidos", "sum"),
        unidades_liquidas=("unidades_liquidas", "sum"),
    )
    resumo["margem_bruta_pct"] = resumo["lucro_bruto"] / resumo["receita_liquida"]
    resumo["margem_contribuicao_pct"] = resumo["contribuicao"] / resumo["receita_liquida"]
    resumo["conversao_pct"] = resumo["pedidos"] / resumo["visitas"]
    return resumo


def curva_abc(dados: pd.DataFrame) -> pd.DataFrame:
    produtos = dados.groupby(["sku", "produto", "categoria"], as_index=False).agg(
        receita_liquida=("receita_liquida", "sum"),
        contribuicao=("contribuicao", "sum"),
        unidades_liquidas=("unidades_liquidas", "sum"),
        unidades_vendidas=("unidades_vendidas", "sum"),
        unidades_devolvidas=("unidades_devolvidas", "sum"),
        semanas_ruptura=("ruptura_estoque", "sum"),
        observacoes=("semana", "size"),
    )
    produtos = produtos.sort_values("receita_liquida", ascending=False).reset_index(drop=True)
    total = produtos["receita_liquida"].sum()
    produtos["participacao_pct"] = produtos["receita_liquida"] / total if total else 0.0
    produtos["participacao_acumulada_pct"] = produtos["participacao_pct"].cumsum()
    produtos["classe_abc"] = np.select(
        [produtos["participacao_acumulada_pct"] <= 0.80, produtos["participacao_acumulada_pct"] <= 0.95],
        ["A", "B"],
        default="C",
    )
    if len(produtos):
        produtos.loc[0, "classe_abc"] = "A"
    produtos["taxa_devolucao_pct"] = produtos["unidades_devolvidas"] / produtos["unidades_vendidas"].replace(0, np.nan)
    produtos["taxa_ruptura_pct"] = produtos["semanas_ruptura"] / produtos["observacoes"]
    return produtos


def principais_insights(dados: pd.DataFrame) -> list[str]:
    categorias = resumo_categoria(dados)
    canais = resumo_canal(dados)
    associacoes = associacoes_volume(dados).sort_values("forca", ascending=False)
    descontos = resumo_desconto(dados)
    top_receita = categorias.iloc[0]
    top_contribuicao = canais.sort_values("margem_contribuicao_pct", ascending=False).iloc[0]
    fator = associacoes.iloc[0]
    melhor_faixa = descontos.sort_values("contribuicao", ascending=False).iloc[0]
    return [
        f"{top_receita['categoria']} lidera a receita líquida no recorte selecionado.",
        f"{top_contribuicao['canal']} apresenta a maior margem de contribuição entre os canais.",
        f"{fator['fator']} tem a associação monotônica mais forte com o volume líquido, com rho de {fator['correlacao_spearman']:.2f}.",
        f"A faixa {melhor_faixa['faixa_desconto']} concentra a maior contribuição total no recorte.",
    ]


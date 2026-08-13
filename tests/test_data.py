import pandas as pd

from src.data import COLUNAS_OBRIGATORIAS, gerar_dados, validar_colunas
from src.metrics import adicionar_metricas


def test_geracao_e_reproduzivel():
    primeira = gerar_dados(semente=42)
    segunda = gerar_dados(semente=42)
    pd.testing.assert_frame_equal(primeira, segunda)
    assert len(primeira) == 52 * 48 * 3
    assert COLUNAS_OBRIGATORIAS.issubset(primeira.columns)


def test_metricas_financeiras_fecham():
    dados = adicionar_metricas(gerar_dados())
    linha = dados.iloc[0]
    assert linha["unidades_liquidas"] == linha["unidades_vendidas"] - linha["unidades_devolvidas"]
    assert round(linha["receita_liquida"], 6) == round(linha["unidades_liquidas"] * linha["preco_liquido"], 6)
    assert dados["margem_bruta_pct"].between(-1, 1).all()
    validar_colunas(dados)


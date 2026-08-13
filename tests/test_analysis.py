from src.analysis import associacoes_volume, calcular_kpis, curva_abc, resumo_desconto
from src.data import gerar_dados
from src.metrics import adicionar_metricas


def base():
    return adicionar_metricas(gerar_dados())


def test_kpis_possuem_resultado_consistente():
    kpis = calcular_kpis(base())
    assert kpis["receita_liquida"] > 0
    assert kpis["lucro_bruto"] > kpis["contribuicao"]
    assert 0 < kpis["conversao_pct"] < 1
    assert 0 < kpis["margem_bruta_pct"] < 1


def test_associacoes_ficam_no_intervalo_valido():
    resultado = associacoes_volume(base())
    assert len(resultado) == 7
    assert resultado["correlacao_spearman"].between(-1, 1).all()


def test_curva_abc_classifica_todos_os_produtos():
    produtos = curva_abc(base())
    assert len(produtos) == 48
    assert set(produtos["classe_abc"]) == {"A", "B", "C"}
    assert abs(produtos["participacao_pct"].sum() - 1) < 1e-9


def test_faixas_de_desconto_sao_ordenadas():
    resultado = resumo_desconto(base())
    assert list(resultado["faixa_desconto"].astype(str)) == ["Sem desconto", "5%", "10%", "15%", "20% ou mais"]


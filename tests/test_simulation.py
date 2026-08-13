from src.data import gerar_dados
from src.metrics import adicionar_metricas
from src.simulation import simular_cenario


def test_reducao_de_preco_eleva_volume_com_elasticidade_negativa():
    dados = adicionar_metricas(gerar_dados())
    recorte = dados[(dados["categoria"] == "Casa e cozinha") & (dados["canal"] == "Site")]
    referencia = simular_cenario(recorte, 0, 10, 0, -1.5)
    promocao = simular_cenario(recorte, 0, 20, 0, -1.5)
    assert promocao["preco_liquido_cenario"] < referencia["preco_liquido_cenario"]
    assert promocao["unidades_cenario"] > referencia["unidades_cenario"]


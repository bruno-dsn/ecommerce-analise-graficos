from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


CATEGORIAS = {
    "Áudio e vídeo": {
        "produtos": ["Fone Pulse", "Caixa Wave", "Webcam Focus", "Microfone Voice", "Soundbar One", "Headset Play"],
        "preco": 340,
        "custo_pct": 0.57,
        "visitas": 215,
        "conversao": 0.028,
        "devolucao": 0.055,
        "elasticidade": 1.75,
    },
    "Casa e cozinha": {
        "produtos": ["Panela Chef", "Air Fryer Easy", "Jogo Mesa", "Luminária Aura", "Organizador Box", "Mixer Prático"],
        "preco": 230,
        "custo_pct": 0.52,
        "visitas": 260,
        "conversao": 0.034,
        "devolucao": 0.035,
        "elasticidade": 1.45,
    },
    "Esporte": {
        "produtos": ["Tênis Run", "Mochila Trail", "Garrafa Move", "Tapete Zen", "Kit Funcional", "Relógio Fit"],
        "preco": 190,
        "custo_pct": 0.49,
        "visitas": 225,
        "conversao": 0.031,
        "devolucao": 0.052,
        "elasticidade": 1.55,
    },
    "Moda": {
        "produtos": ["Camiseta Urban", "Calça Flex", "Tênis Street", "Jaqueta City", "Bolsa Mini", "Moletom Soft"],
        "preco": 150,
        "custo_pct": 0.43,
        "visitas": 315,
        "conversao": 0.037,
        "devolucao": 0.105,
        "elasticidade": 1.9,
    },
    "Beleza": {
        "produtos": ["Kit Skin", "Perfume Bloom", "Secador Air", "Protetor Daily", "Escova Glow", "Sérum Vita"],
        "preco": 115,
        "custo_pct": 0.39,
        "visitas": 290,
        "conversao": 0.041,
        "devolucao": 0.026,
        "elasticidade": 1.35,
    },
    "Informática": {
        "produtos": ["Teclado Type", "Mouse Click", "Monitor View", "SSD Fast", "Hub Connect", "Notebook Go"],
        "preco": 520,
        "custo_pct": 0.66,
        "visitas": 185,
        "conversao": 0.023,
        "devolucao": 0.045,
        "elasticidade": 2.05,
    },
    "Infantil": {
        "produtos": ["Bloco Criar", "Livro Descobrir", "Jogo Família", "Mochila Kids", "Pelúcia Nuvem", "Patinete Joy"],
        "preco": 125,
        "custo_pct": 0.47,
        "visitas": 205,
        "conversao": 0.036,
        "devolucao": 0.032,
        "elasticidade": 1.5,
    },
    "Pet": {
        "produtos": ["Cama Cozy", "Fonte Fresh", "Brinquedo Fun", "Coleira Safe", "Comedouro Smart", "Kit Higiene"],
        "preco": 105,
        "custo_pct": 0.44,
        "visitas": 235,
        "conversao": 0.039,
        "devolucao": 0.022,
        "elasticidade": 1.25,
    },
}

CANAIS = {
    "Site": {"trafego": 1.0, "conversao": 1.0, "taxa_pct": 0.025, "prazo": 3.2},
    "Aplicativo": {"trafego": 0.82, "conversao": 1.16, "taxa_pct": 0.02, "prazo": 3.0},
    "Marketplace": {"trafego": 1.18, "conversao": 0.94, "taxa_pct": 0.145, "prazo": 4.1},
}

COLUNAS_OBRIGATORIAS = {
    "semana",
    "sku",
    "produto",
    "categoria",
    "canal",
    "preco_lista",
    "desconto_pct",
    "custo_unitario",
    "visitas",
    "pedidos",
    "unidades_vendidas",
    "unidades_devolvidas",
    "investimento_midia",
    "avaliacao_media",
    "prazo_entrega_dias",
    "estoque_inicial",
}


def _fator_sazonal(data: pd.Timestamp) -> float:
    mes = data.month
    if mes == 11:
        return 1.58
    if mes == 12:
        return 1.28
    if mes in {5, 6}:
        return 1.12
    if mes in {1, 2}:
        return 0.88
    return 1.0


def gerar_dados(semente: int = 42) -> pd.DataFrame:
    """Gera uma base semanal sintética, reproduzível e coerente com o negócio."""
    rng = np.random.default_rng(semente)
    semanas = pd.date_range("2025-01-06", "2025-12-29", freq="W-MON")
    linhas: list[dict[str, object]] = []

    catalogo: list[dict[str, object]] = []
    contador = 1
    for categoria, config in CATEGORIAS.items():
        for produto in config["produtos"]:
            catalogo.append(
                {
                    "sku": f"SKU{contador:03d}",
                    "produto": produto,
                    "categoria": categoria,
                    "popularidade": float(np.clip(rng.lognormal(mean=0.0, sigma=0.52), 0.38, 2.20)),
                    "fator_preco": float(rng.uniform(0.76, 1.34)),
                    "nota_base": float(rng.uniform(3.55, 4.88)),
                }
            )
            contador += 1

    for semana in semanas:
        sazonalidade = _fator_sazonal(semana)
        for item in catalogo:
            categoria = str(item["categoria"])
            config = CATEGORIAS[categoria]
            for canal, config_canal in CANAIS.items():
                novembro = semana.month == 11
                descontos = [0, 5, 10, 15, 20, 25, 30]
                probabilidades = [0.20, 0.18, 0.24, 0.18, 0.12, 0.06, 0.02]
                if novembro:
                    probabilidades = [0.03, 0.07, 0.14, 0.22, 0.25, 0.19, 0.10]
                desconto = int(rng.choice(descontos, p=probabilidades))

                preco_lista = (
                    float(config["preco"])
                    * float(item["fator_preco"])
                    * float(rng.normal(1.0, 0.025))
                )
                preco_liquido = preco_lista * (1 - desconto / 100)
                custo_unitario = (
                    float(config["preco"])
                    * float(item["fator_preco"])
                    * float(config["custo_pct"])
                    * float(rng.normal(1.0, 0.018))
                )

                campanha = float(rng.lognormal(mean=0.0, sigma=0.28))
                investimento_midia = 290 * campanha * float(config_canal["trafego"]) * sazonalidade
                visitas_esperadas = (
                    float(config["visitas"])
                    * float(item["popularidade"])
                    * float(config_canal["trafego"])
                    * sazonalidade
                    * (0.82 + 0.18 * campanha)
                )
                visitas = max(25, int(rng.poisson(visitas_esperadas)))

                avaliacao = float(np.clip(float(item["nota_base"]) + rng.normal(0, 0.11), 3.1, 5.0))
                prazo = float(np.clip(float(config_canal["prazo"]) + rng.normal(0, 0.55), 1.2, 7.5))
                indice_preco = preco_liquido / (float(config["preco"]) * float(item["fator_preco"]))
                efeito_preco = indice_preco ** (-float(config["elasticidade"]))
                efeito_nota = 1 + (avaliacao - 4.0) * 0.30
                efeito_prazo = np.exp(-0.13 * (prazo - 3.0))
                conversao = (
                    float(config["conversao"])
                    * float(config_canal["conversao"])
                    * efeito_preco
                    * efeito_nota
                    * efeito_prazo
                    * float(rng.normal(1.0, 0.065))
                )
                conversao = float(np.clip(conversao, 0.006, 0.105))
                pedidos = int(rng.binomial(visitas, conversao))
                demanda_unidades = pedidos + int(rng.binomial(pedidos, 0.14))

                risco_ruptura = rng.random() < (0.055 + 0.075 * (sazonalidade > 1.4))
                cobertura = float(rng.uniform(0.62, 0.96) if risco_ruptura else rng.uniform(1.08, 1.65))
                estoque = max(1, int(np.ceil(max(visitas * conversao, 1) * 1.14 * cobertura)))
                unidades_vendidas = min(demanda_unidades, estoque)
                taxa_devolucao = float(config["devolucao"]) * (1 + max(0, 4.1 - avaliacao) * 0.18)
                devolvidas = int(rng.binomial(unidades_vendidas, min(taxa_devolucao, 0.18)))

                linhas.append(
                    {
                        "semana": semana.date().isoformat(),
                        "sku": item["sku"],
                        "produto": item["produto"],
                        "categoria": categoria,
                        "canal": canal,
                        "preco_lista": round(preco_lista, 2),
                        "desconto_pct": desconto,
                        "custo_unitario": round(custo_unitario, 2),
                        "visitas": visitas,
                        "pedidos": pedidos,
                        "unidades_vendidas": unidades_vendidas,
                        "unidades_devolvidas": devolvidas,
                        "investimento_midia": round(investimento_midia, 2),
                        "avaliacao_media": round(avaliacao, 2),
                        "prazo_entrega_dias": round(prazo, 2),
                        "estoque_inicial": estoque,
                    }
                )

    return pd.DataFrame(linhas)


def salvar_dados(caminho: str | Path, semente: int = 42) -> pd.DataFrame:
    dados = gerar_dados(semente=semente)
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    dados.to_csv(destino, index=False)
    return dados


def carregar_dados(origem: str | Path | object) -> pd.DataFrame:
    dados = pd.read_csv(origem, parse_dates=["semana"])
    validar_colunas(dados)
    return dados


def validar_colunas(dados: pd.DataFrame) -> None:
    faltantes = COLUNAS_OBRIGATORIAS - set(dados.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes: {', '.join(sorted(faltantes))}")

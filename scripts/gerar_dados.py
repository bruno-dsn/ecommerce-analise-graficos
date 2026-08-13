from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.data import salvar_dados


if __name__ == "__main__":
    dados = salvar_dados(RAIZ / "data" / "ecommerce_2025.csv")
    print(f"Base criada com {len(dados):,} linhas em data/ecommerce_2025.csv")


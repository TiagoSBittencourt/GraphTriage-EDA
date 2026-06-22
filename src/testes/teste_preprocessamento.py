import sys
from pathlib import Path
import json

# adiciona src no path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.preprocessamento import preprocessar


# caminho do dataset
BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = BASE_DIR / "data" / "corpus.json"


def carregar_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def testar_dataset():
    dados = carregar_dataset()

    print("\n==============================")
    print("TESTE COM DATASET COMPLETO")
    print("==============================\n")

    for i, item in enumerate(dados[:20], 1):  # primeiros 20 para não poluir
        texto = item.get("texto") or item.get("queixa") or item.get("sentence")
        label = item.get("categoria", "NAO_ROTULADO")

        tokens = preprocessar(texto)

        print(f"CASO {i}")
        print("Original   :", texto)
        print("Categoria   :", label)
        print("Processado  :", tokens)
        print("-" * 50)


if __name__ == "__main__":
    testar_dataset()
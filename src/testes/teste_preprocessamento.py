import sys
from pathlib import Path

# adiciona src no path (igual seu teste do grafo)
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.preprocessamento import preprocessar


def testar():
    casos = [
        "Dor no peito e falta de ar há 2 dias",
        "Paciente relata dores fortes no joelho esquerdo",
        "Apresenta náuseas e vômitos desde ontem",
        "Falta de ar e dor no peito ao caminhar",
        "Tontura e dor de cabeça persistente"
    ]

    for i, texto in enumerate(casos, 1):
        print(f"\nCASO {i}")
        print("Original:", texto)
        print("Processado:", preprocessar(texto))
        print("-" * 50)


if __name__ == "__main__":
    testar()
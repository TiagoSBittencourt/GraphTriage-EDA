"""
Gera o logo do GraphTriage (assets/logo.png).

O logo representa o grafo tripartite do projeto: um nó central vermelho
(categoria), nós azuis nos braços (documentos) e nós verdes satélites
(termos), formando uma rede em cruz — alusão à triagem médica.

Uso: python assets/gerar_logo.py
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Paleta do projeto (mesma das visualizações)
AZUL = "#4A90D9"   # documento
VERDE = "#2ECC71"  # termo
VERM = "#E74C3C"   # categoria
BRANCO = "#FFFFFF"


def gerar(caminho: str = "assets/logo.png") -> None:
    fig = plt.figure(figsize=(8, 8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.axis("off")

    # Fundo gradiente (navy -> teal) recortado em retângulo arredondado
    grad = np.zeros((256, 256, 3))
    top = np.array([15, 32, 39]) / 255
    mid = np.array([32, 58, 67]) / 255
    bot = np.array([44, 83, 100]) / 255
    for i in range(256):
        t = i / 255
        grad[i, :, :] = top + (mid - top) * (t / 0.5) if t < 0.5 else mid + (bot - mid) * ((t - 0.5) / 0.5)
    bg = ax.imshow(grad[::-1], extent=[-5, 5, -5, 5], origin="upper", zorder=0)
    box = FancyBboxPatch((-4.6, -4.6), 9.2, 9.2,
                         boxstyle="round,pad=0,rounding_size=1.8",
                         transform=ax.transData, facecolor="none", edgecolor="none")
    bg.set_clip_path(box)
    ax.add_patch(box)

    # Nós: centro (categoria), braços (documentos), satélites (termos)
    centro = (0, 0)
    bracos = {"cima": (0, 2.6), "baixo": (0, -2.6), "esq": (-2.6, 0), "dir": (2.6, 0)}
    satelites = [(-2.1, 2.1), (2.1, 2.1), (-2.1, -2.1), (2.1, -2.1)]

    def aresta(p, q, lw, alpha, color):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, alpha=alpha,
                solid_capstyle="round", zorder=2)

    for b in bracos.values():
        aresta(centro, b, 6, 0.85, "#9FE7FF")
    ligacoes = [
        (satelites[0], bracos["cima"]), (satelites[0], bracos["esq"]),
        (satelites[1], bracos["cima"]), (satelites[1], bracos["dir"]),
        (satelites[2], bracos["baixo"]), (satelites[2], bracos["esq"]),
        (satelites[3], bracos["baixo"]), (satelites[3], bracos["dir"]),
    ]
    for p, q in ligacoes:
        aresta(p, q, 3, 0.5, "#8FE3B0")

    def no(p, r, color):
        ax.scatter(*p, s=(r * 1.9) ** 2 * 90, c=color, alpha=0.20, zorder=3, edgecolors="none")
        ax.scatter(*p, s=r ** 2 * 90, c=color, zorder=4, edgecolors=BRANCO, linewidths=3.2)

    for s in satelites:
        no(s, 3.4, VERDE)
    for b in bracos.values():
        no(b, 4.6, AZUL)
    no(centro, 6.6, VERM)

    fig.savefig(caminho, transparent=True, dpi=100)
    plt.close(fig)
    print(f"Logo salvo em {caminho}")


if __name__ == "__main__":
    gerar()

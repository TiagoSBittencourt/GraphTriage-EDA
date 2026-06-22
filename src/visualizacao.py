"""
Visualização do grafo e propagação de rótulos.
Issue: #8
"""

import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import Normalize

from .grafo import Grafo
from .label_propagation import LabelPropagation
from .indice_invertido import IndiceInvertido


CORES_TIPO = {
    "documento": "#4A90D9",
    "termo": "#2ECC71",
    "categoria": "#E74C3C",
}

CORES_CATEGORIA = {
    "Cardiologia": "#E74C3C",
    "Ortopedia": "#3498DB",
    "Neurologia": "#9B59B6",
    "Dermatologia": "#E67E22",
    "Gastroenterologia": "#1ABC9C",
}


def _garantir_diretorio(caminho: str) -> None:
    os.makedirs(os.path.dirname(caminho), exist_ok=True)


def plotar_grafo(
    grafo: Grafo,
    indice: IndiceInvertido,
    rotulos: dict[str, str],
    top_termos: int = 5,
    salvar_em: str = "docs/plots/grafo.png",
) -> None:
    """Plot 1: Grafo estático tripartite com top-N termos por categoria."""
    _garantir_diretorio(salvar_em)

    categorias = grafo.get_vertices_por_tipo("categoria")
    top = indice.top_termos_por_categoria(rotulos, n=top_termos)
    termos_selecionados: set[str] = set()
    for lista in top.values():
        for termo, _ in lista:
            termos_selecionados.add(termo)

    docs_selecionados: set[str] = set()
    for termo in termos_selecionados:
        vizinhos = grafo.get_vizinhos(termo)
        for v in vizinhos:
            if grafo.get_tipo(v) == "documento":
                docs_selecionados.add(v)
                if len(docs_selecionados) >= 40:
                    break
        if len(docs_selecionados) >= 40:
            break

    vertices = list(categorias) + list(termos_selecionados) + list(docs_selecionados)
    vertices_set = set(vertices)

    pos: dict[str, tuple[float, float]] = {}
    n_cats = len(categorias)
    for i, cat in enumerate(categorias):
        x = (i - n_cats / 2 + 0.5) * 3.0
        pos[cat] = (x, 4.0)

    termos_lista = sorted(termos_selecionados)
    n_termos = len(termos_lista)
    for i, t in enumerate(termos_lista):
        x = (i - n_termos / 2 + 0.5) * 1.5
        pos[t] = (x, 0.0)

    docs_lista = sorted(docs_selecionados)
    n_docs = len(docs_lista)
    for i, d in enumerate(docs_lista):
        x = (i - n_docs / 2 + 0.5) * 0.8
        pos[d] = (x, -4.0)

    fig, ax = plt.subplots(figsize=(18, 12))

    peso_max = 1.0
    arestas = []
    for v in vertices:
        for u, peso in grafo.get_vizinhos(v).items():
            if u in vertices_set and (u, v) not in {(a, b) for a, b, _ in arestas}:
                arestas.append((v, u, peso))
                peso_max = max(peso_max, peso)

    for v, u, peso in arestas:
        lw = 0.3 + 2.5 * (peso / peso_max)
        ax.plot(
            [pos[v][0], pos[u][0]],
            [pos[v][1], pos[u][1]],
            color="#CCCCCC",
            linewidth=lw,
            alpha=0.5,
            zorder=1,
        )

    for v in vertices:
        tipo = grafo.get_tipo(v)
        cor = CORES_TIPO[tipo]
        tamanho = {"categoria": 500, "termo": 200, "documento": 60}[tipo]
        ax.scatter(pos[v][0], pos[v][1], s=tamanho, c=cor, zorder=2, edgecolors="white", linewidths=0.5)
        if tipo != "documento":
            fontsize = 11 if tipo == "categoria" else 7
            fontweight = "bold" if tipo == "categoria" else "normal"
            ax.annotate(
                v,
                pos[v],
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                fontsize=fontsize,
                fontweight=fontweight,
                zorder=3,
            )

    legendas = [
        mpatches.Patch(color=CORES_TIPO["categoria"], label="Categoria"),
        mpatches.Patch(color=CORES_TIPO["termo"], label="Termo"),
        mpatches.Patch(color=CORES_TIPO["documento"], label="Documento"),
    ]
    ax.legend(handles=legendas, loc="upper right", fontsize=10)
    ax.set_title(
        f"Grafo Tripartite (top-{top_termos} termos por categoria)",
        fontsize=14,
        fontweight="bold",
    )
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(salvar_em, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Plot 1 salvo em {salvar_em}")


def plotar_evolucao_scores(
    historico: list[dict],
    doc_id: str,
    categorias: list[str] | None = None,
    salvar_em: str = "docs/plots/evolucao_scores.png",
) -> None:
    """Plot 2: Evolução dos scores por iteração para um documento."""
    _garantir_diretorio(salvar_em)

    if categorias is None:
        cats: set[str] = set()
        for snapshot in historico:
            if doc_id in snapshot:
                cats.update(snapshot[doc_id].keys())
        categorias = sorted(cats)

    iteracoes = list(range(len(historico)))
    fig, ax = plt.subplots(figsize=(10, 6))

    for cat in categorias:
        valores = [snapshot.get(doc_id, {}).get(cat, 0.0) for snapshot in historico]
        cor = CORES_CATEGORIA.get(cat, "#888888")
        ax.plot(iteracoes, valores, label=cat, color=cor, linewidth=2, marker="o", markersize=3)

    ax.set_xlabel("Iteracao", fontsize=12)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title(f"Evolucao dos scores — {doc_id}", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(salvar_em, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Plot 2 salvo em {salvar_em}")


def plotar_heatmap_scores(
    lp: LabelPropagation,
    docs_nao_rotulados: list[str],
    categorias: list[str],
    salvar_em: str = "docs/plots/heatmap_scores.png",
) -> None:
    """Plot 3: Heatmap de scores finais (docs x categorias)."""
    _garantir_diretorio(salvar_em)

    n_docs = len(docs_nao_rotulados)
    n_cats = len(categorias)

    matriz = []
    previstos = []
    for doc in docs_nao_rotulados:
        linha = [lp.scores.get(doc, {}).get(cat, 0.0) for cat in categorias]
        matriz.append(linha)
        cat_prev, _ = lp.predict(doc)
        previstos.append(cat_prev)

    fig_height = max(8, n_docs * 0.22)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    im = ax.imshow(matriz, aspect="auto", cmap="YlOrRd", interpolation="nearest")

    for i in range(n_docs):
        for j in range(n_cats):
            valor = matriz[i][j]
            cor_texto = "white" if valor > 0.4 else "black"
            fontweight = "bold" if categorias[j] == previstos[i] else "normal"
            ax.text(j, i, f"{valor:.2f}", ha="center", va="center",
                    fontsize=6, color=cor_texto, fontweight=fontweight)
            if categorias[j] == previstos[i]:
                rect = plt.Rectangle(
                    (j - 0.5, i - 0.5), 1, 1,
                    linewidth=2, edgecolor="black", facecolor="none"
                )
                ax.add_patch(rect)

    ax.set_xticks(range(n_cats))
    ax.set_xticklabels(categorias, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(n_docs))
    ax.set_yticklabels(docs_nao_rotulados, fontsize=6)
    ax.set_xlabel("Categoria", fontsize=12)
    ax.set_ylabel("Documento", fontsize=12)
    ax.set_title("Scores Finais — Label Propagation", fontsize=14, fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, shrink=0.6)
    cbar.set_label("Score", fontsize=10)

    fig.tight_layout()
    fig.savefig(salvar_em, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Plot 3 salvo em {salvar_em}")

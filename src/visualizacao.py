"""
Visualização do grafo e propagação de rótulos.
Issue: #8 e #9
"""


def plotar_grafo(grafo, top_termos: int = 5, salvar_em: str = "docs/plots/grafo.png"):
    # TODO (issue #8): implementar com matplotlib
    raise NotImplementedError


def plotar_evolucao_scores(
    historico: list[dict],
    doc_id: str,
    salvar_em: str = "docs/plots/evolucao_scores.png",
):
    # TODO (issue #8): plotar scores por iteração para doc_id
    raise NotImplementedError


def plotar_heatmap_scores(
    lp,
    docs_nao_rotulados: list[str],
    categorias: list[str],
    salvar_em: str = "docs/plots/heatmap_scores.png",
):
    # TODO (issue #8): heatmap scores finais
    raise NotImplementedError


def plotar_termos_por_categoria(
    grafo,
    top_n: int = 10,
    salvar_em: str = "docs/plots/termos_por_categoria.png",
):
    # TODO (issue #9): bar chart horizontal de termos por categoria
    raise NotImplementedError

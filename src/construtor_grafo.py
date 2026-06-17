"""
Monta o grafo tripartite Documento–Termo–Categoria.
Issue: #5
"""

from .grafo import Grafo
from .indice_invertido import IndiceInvertido


def construir_grafo(
    documentos: list[dict],
    rotulos: dict[str, str],
    indice: IndiceInvertido,
) -> Grafo:
    g = Grafo()

    for doc in documentos:
        g.adicionar_vertice(doc["id"], tipo="documento")

    for termo in indice.termos():
        g.adicionar_vertice(termo, tipo="termo")

    categorias = set(rotulos.values())
    for cat in categorias:
        g.adicionar_vertice(cat, tipo="categoria")

    # Aresta Documento↔Termo (peso = frequência do termo no doc)
    for doc in documentos:
        for termo in indice.termos():
            freq = indice.frequencia_no_doc(termo, doc["id"])
            if freq > 0:
                g.adicionar_aresta(doc["id"], termo, peso=float(freq))

    # Aresta Termo↔Categoria (peso = nº de docs da categoria com o termo)
    for termo in indice.termos():
        for cat, contagem in indice.contagem_por_categoria(termo, rotulos).items():
            if contagem > 0:
                g.adicionar_aresta(termo, cat, peso=float(contagem))

    # Aresta Documento↔Categoria (peso = 1.0, apenas rotulados)
    for doc_id, cat in rotulos.items():
        g.adicionar_aresta(doc_id, cat, peso=1.0)

    return g

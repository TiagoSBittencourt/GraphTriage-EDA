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
    n_doc_termo = 0
    for doc in documentos:
        for termo in indice.termos():
            freq = indice.frequencia_no_doc(termo, doc["id"])
            if freq > 0:
                g.adicionar_aresta(doc["id"], termo, peso=float(freq))
                n_doc_termo += 1

    # Aresta Termo↔Categoria
    # peso = (nº de docs da categoria com o termo) × IDF(termo)
    # O fator IDF reduz a influência de termos genéricos (ex.: "dor"), que
    # aparecem em muitas categorias, e valoriza termos discriminativos.
    n_termo_cat = 0
    for termo in indice.termos():
        idf = indice.idf(termo)
        for cat, contagem in indice.contagem_por_categoria(termo, rotulos).items():
            if contagem > 0:
                g.adicionar_aresta(termo, cat, peso=float(contagem) * idf)
                n_termo_cat += 1

    # Aresta Documento↔Categoria (peso = 1.0, apenas rotulados)
    n_doc_cat = 0
    for doc_id, cat in rotulos.items():
        g.adicionar_aresta(doc_id, cat, peso=1.0)
        n_doc_cat += 1

    docs = len(g.get_vertices_por_tipo("documento"))
    termos = len(g.get_vertices_por_tipo("termo"))
    cats = len(g.get_vertices_por_tipo("categoria"))
    print(f"\n=== Grafo tripartite construído ===")
    print(f"Vértices : {docs} documentos | {termos} termos | {cats} categorias")
    print(f"Arestas  : {n_doc_termo} Documento↔Termo | {n_termo_cat} Termo↔Categoria | {n_doc_cat} Documento↔Categoria")

    return g

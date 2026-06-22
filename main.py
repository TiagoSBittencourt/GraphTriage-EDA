"""
Pipeline principal do GraphTriage-EDA.
"""

import json
from src.indice_invertido import IndiceInvertido
from src.construtor_grafo import construir_grafo
from src.label_propagation import LabelPropagation
from src.avaliacao import holdout_split, avaliar, imprimir_relatorio


def carregar_corpus(caminho: str = "data/corpus.json") -> list[dict]:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def carregar_gabarito(caminho: str = "data/corpus-rotulado.json") -> dict[str, str]:
    """Mapa id -> categoria real das queixas não rotuladas (gabarito)."""
    with open(caminho, encoding="utf-8") as f:
        return {d["id"]: d["categoria_real"] for d in json.load(f)}


def main():
    documentos = carregar_corpus()
    gabarito = carregar_gabarito()

    rotulados = [d for d in documentos if d["categoria"]]
    nao_rotulados = [d for d in documentos if not d["categoria"]]

    treino, teste = holdout_split(rotulados)
    rotulos_treino = {d["id"]: d["categoria"] for d in treino}

    todos = treino + teste + nao_rotulados

    indice = IndiceInvertido()
    indice.construir(todos)
    indice.imprimir_top_termos(rotulos_treino)

    grafo = construir_grafo(todos, rotulos_treino, indice)
    print(grafo)

    lp = LabelPropagation()
    lp.fit(grafo, rotulos_treino)

    print("\n=== Classificação de queixas não rotuladas ===")
    for doc in nao_rotulados:
        cat, score = lp.predict(doc["id"])
        gab = gabarito.get(doc["id"], "?")
        marca = "✓" if cat == gab else "✗"
        print(f"  {doc['id']}: {cat} (score={score}) | real: {gab} {marca}")

    # Avaliação 1: holdout sobre documentos rotulados
    print("\n############ HOLDOUT (documentos rotulados) ############")
    metricas = avaliar(lp, teste)
    imprimir_relatorio(metricas)

    # Avaliação 2: queixas ambíguas não rotuladas contra o gabarito
    docs_ambiguos = [
        {"id": doc["id"], "categoria": gabarito[doc["id"]]}
        for doc in nao_rotulados
        if doc["id"] in gabarito
    ]
    if docs_ambiguos:
        print("\n####### QUEIXAS AMBÍGUAS (gabarito U*) #######")
        metricas_amb = avaliar(lp, docs_ambiguos)
        imprimir_relatorio(metricas_amb)


if __name__ == "__main__":
    main()

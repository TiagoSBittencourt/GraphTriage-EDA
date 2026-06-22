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


def main():
    documentos = carregar_corpus()

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
        print(f"  {doc['id']}: {cat} (score={score})")

    metricas = avaliar(lp, teste)
    imprimir_relatorio(metricas)


if __name__ == "__main__":
    main()

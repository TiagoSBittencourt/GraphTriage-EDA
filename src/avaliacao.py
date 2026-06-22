"""
Módulo de avaliação e métricas (holdout + acurácia + matriz de confusão).
Issue: #7
"""

import random
from .label_propagation import LabelPropagation


def holdout_split(
    documentos: list[dict], frac_teste: float = 0.2, seed: int = 42
) -> tuple[list[dict], list[dict]]:
    rotulados = [d for d in documentos if d["categoria"]]

    por_cat: dict[str, list[dict]] = {}
    for d in rotulados:
        por_cat.setdefault(d["categoria"], []).append(d)

    rng = random.Random(seed)
    treino, teste = [], []
    for docs in por_cat.values():
        rng.shuffle(docs)
        n_teste = max(1, round(len(docs) * frac_teste))
        teste.extend(docs[:n_teste])
        treino.extend(docs[n_teste:])

    return treino, teste


def avaliar(lp: LabelPropagation, docs_teste: list[dict]) -> dict:
    categorias = sorted({d["categoria"] for d in docs_teste})
    matriz: dict[str, dict[str, int]] = {c: {c2: 0 for c2 in categorias} for c in categorias}
    erros_confiantes: list[dict] = []
    acertos = 0

    for doc in docs_teste:
        real = doc["categoria"]
        previsto, confianca = lp.predict(doc["id"])
        matriz[real][previsto] = matriz[real].get(previsto, 0) + 1
        if previsto == real:
            acertos += 1
        else:
            erros_confiantes.append(
                {"id": doc["id"], "previsto": previsto, "real": real, "confianca": confianca}
            )

    erros_confiantes.sort(key=lambda x: x["confianca"], reverse=True)

    acuracia_por_cat = {}
    for cat in categorias:
        total = sum(matriz[cat].values())
        acuracia_por_cat[cat] = matriz[cat].get(cat, 0) / total if total else 0.0

    return {
        "acuracia_geral": acertos / len(docs_teste) if docs_teste else 0.0,
        "acuracia_por_categoria": acuracia_por_cat,
        "matriz_confusao": matriz,
        "erros_confiantes": erros_confiantes[:5],
    }


def imprimir_relatorio(metricas: dict) -> None:
    print(f"\n=== Avaliação ===")
    print(f"Acurácia geral: {metricas['acuracia_geral']:.1%}\n")
    print("Por categoria:")
    for cat, acc in metricas["acuracia_por_categoria"].items():
        print(f"  {cat:<20}: {acc:.1%}")

    print("\nMatriz de confusão:")
    matriz = metricas["matriz_confusao"]
    cats = list(matriz.keys())
    col_w = max(8, max(len(c) for c in cats))
    print(" " * (col_w + 2) + "".join(f"{c:>{col_w}}" for c in cats))
    for real in cats:
        valores = "".join(f"{matriz[real].get(prev, 0):>{col_w}}" for prev in cats)
        print(f"  {real:<{col_w}}{valores}")

    print("\nErros mais confiantes:")
    for e in metricas["erros_confiantes"]:
        print(f"  {e['id']} → previsto: {e['previsto']} ({e['confianca']:.2f}) | real: {e['real']}")

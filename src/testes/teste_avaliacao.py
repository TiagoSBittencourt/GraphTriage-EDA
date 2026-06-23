"""
Testes do módulo de avaliação e métricas (issue #7).

Execução: python -m src.testes.teste_avaliacao
"""

from src.avaliacao import holdout_split, avaliar


def teste_holdout_split_estratificado_e_deterministico():
    docs = [{"id": f"Q{i}", "categoria": "A" if i % 2 == 0 else "B"} for i in range(10)]
    treino1, teste1 = holdout_split(docs, frac_teste=0.2, seed=42)
    treino2, teste2 = holdout_split(docs, frac_teste=0.2, seed=42)

    # determinístico
    assert [d["id"] for d in teste1] == [d["id"] for d in teste2]
    # nenhuma sobreposição treino/teste
    ids_treino = {d["id"] for d in treino1}
    ids_teste = {d["id"] for d in teste1}
    assert ids_treino.isdisjoint(ids_teste)
    # cada categoria representada no teste (estratificação)
    cats_teste = {d["categoria"] for d in teste1}
    assert cats_teste == {"A", "B"}


class _LPFake:
    """Stub de classificador: devolve predições fixas para testar 'avaliar'."""
    def __init__(self, predicoes):
        self._p = predicoes

    def predict(self, doc_id):
        return self._p[doc_id]


def teste_avaliar_metricas():
    docs = [
        {"id": "Q1", "categoria": "A"},
        {"id": "Q2", "categoria": "A"},
        {"id": "Q3", "categoria": "B"},
        {"id": "Q4", "categoria": "B"},
    ]
    lp = _LPFake({
        "Q1": ("A", 0.9),
        "Q2": ("B", 0.7),   # erro
        "Q3": ("B", 0.8),
        "Q4": ("B", 0.6),
    })
    m = avaliar(lp, docs)
    assert m["acuracia_geral"] == 0.75            # 3/4 corretos
    assert m["acuracia_por_categoria"]["A"] == 0.5
    assert m["acuracia_por_categoria"]["B"] == 1.0
    assert m["matriz_confusao"]["A"]["B"] == 1    # Q2: real A, previsto B
    assert m["erros_confiantes"][0]["id"] == "Q2"


def teste_avaliar_corpus_vazio():
    lp = _LPFake({})
    m = avaliar(lp, [])
    assert m["acuracia_geral"] == 0.0


def main():
    testes = [v for k, v in globals().items() if k.startswith("teste_")]
    for t in testes:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(testes)} testes de avaliação passaram.")


if __name__ == "__main__":
    main()

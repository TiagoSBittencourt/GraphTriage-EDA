"""
Testes do algoritmo de Label Propagation (issue #6).

Execução: python -m src.testes.teste_label_propagation
"""

from src.indice_invertido import IndiceInvertido
from src.construtor_grafo import construir_grafo
from src.label_propagation import LabelPropagation


def _pipeline_minima():
    """Corpus mínimo, separável: 2 docs por categoria + 1 ambíguo claro."""
    docs = [
        {"id": "Q1", "texto": "dor no peito e palpitação", "categoria": "Cardiologia"},
        {"id": "Q2", "texto": "falta de ar e palpitação no peito", "categoria": "Cardiologia"},
        {"id": "Q3", "texto": "dor no joelho ao caminhar", "categoria": "Ortopedia"},
        {"id": "Q4", "texto": "inchaço no joelho e no tornozelo", "categoria": "Ortopedia"},
        {"id": "U1", "texto": "palpitação no peito", "categoria": ""},   # -> Cardiologia
    ]
    rotulos = {d["id"]: d["categoria"] for d in docs if d["categoria"]}
    idx = IndiceInvertido()
    idx.construir(docs)
    grafo = construir_grafo(docs, rotulos, idx)
    lp = LabelPropagation()
    lp.fit(grafo, rotulos)
    return lp


def teste_rotulos_de_treino_permanecem_fixos():
    lp = _pipeline_minima()
    cat, score = lp.predict("Q1")
    assert cat == "Cardiologia"
    assert score == 1.0  # rótulo conhecido nunca muda


def teste_classifica_nao_rotulado_corretamente():
    lp = _pipeline_minima()
    cat, score = lp.predict("U1")
    assert cat == "Cardiologia"
    assert 0.0 < score <= 1.0


def teste_predict_documento_inexistente():
    lp = _pipeline_minima()
    cat, score = lp.predict("NAO_EXISTE")
    assert cat == "indefinido"
    assert score == 0.0


def teste_historico_registra_iteracoes():
    lp = _pipeline_minima()
    # snapshot inicial + ao menos uma iteração
    assert len(lp.historico_scores) >= 2


def main():
    testes = [v for k, v in globals().items() if k.startswith("teste_")]
    for t in testes:
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(testes)} testes do Label Propagation passaram.")


if __name__ == "__main__":
    main()

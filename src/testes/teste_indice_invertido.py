"""
Testes do índice invertido e da contagem de co-ocorrência (issue #4).

Execução: python -m src.testes.teste_indice_invertido
"""

import math

from src.indice_invertido import IndiceInvertido


def _indice_exemplo():
    docs = [
        {"id": "Q1", "texto": "dor no peito", "categoria": "Cardiologia"},
        {"id": "Q2", "texto": "dor no peito e palpitação", "categoria": "Cardiologia"},
        {"id": "Q3", "texto": "dor no joelho", "categoria": "Ortopedia"},
    ]
    idx = IndiceInvertido()
    idx.construir(docs)
    rotulos = {d["id"]: d["categoria"] for d in docs}
    return idx, rotulos


def teste_frequencia_no_doc():
    idx, _ = _indice_exemplo()
    assert idx.frequencia_no_doc("dor", "Q1") == 1
    assert idx.frequencia_no_doc("inexistente", "Q1") == 0


def teste_get_docs():
    idx, _ = _indice_exemplo()
    # o índice armazena os radicais (stems): "joelho" -> "joelh"
    assert set(idx.get_docs("dor")) == {"Q1", "Q2", "Q3"}
    assert set(idx.get_docs("joelh")) == {"Q3"}


def teste_frequencia_documento():
    idx, _ = _indice_exemplo()
    assert idx.frequencia_documento("dor") == 3   # presente nos 3 docs
    assert idx.frequencia_documento("joelh") == 1


def teste_idf_discrimina_termos():
    idx, _ = _indice_exemplo()
    # "dor" aparece em todos -> IDF menor que "joelh" (raro)
    assert idx.idf("dor") < idx.idf("joelh")
    # valor esperado para "dor": log((3+1)/(3+1)) + 1 = 1.0
    assert math.isclose(idx.idf("dor"), 1.0)


def teste_contagem_por_categoria():
    idx, rotulos = _indice_exemplo()
    cont = idx.contagem_por_categoria("dor", rotulos)
    assert cont == {"Cardiologia": 2, "Ortopedia": 1}


def teste_top_termos_por_categoria():
    idx, rotulos = _indice_exemplo()
    top = idx.top_termos_por_categoria(rotulos, n=2)
    termos_cardio = {t for t, _ in top["Cardiologia"]}
    assert "peit" in termos_cardio or "dor" in termos_cardio  # radicais (stems)


def main():
    testes = [v for k, v in globals().items() if k.startswith("teste_")]
    for t in testes:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(testes)} testes do índice invertido passaram.")


if __name__ == "__main__":
    main()

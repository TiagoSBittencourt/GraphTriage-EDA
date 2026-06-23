"""
Testes do módulo de pré-processamento (issue #2).

Execução: python -m src.testes.teste_preprocessamento
"""

from src.preprocessamento import tokenizar, remover_stopwords, normalizar, preprocessar


def teste_tokenizar_minusculas_e_pontuacao():
    assert tokenizar("Dor no PEITO, há 2 dias!") == ["dor", "no", "peito", "há", "2", "dias"]


def teste_remover_stopwords():
    tokens = ["dor", "no", "peito", "e", "falta", "de", "ar"]
    assert "no" not in remover_stopwords(tokens)
    assert "de" not in remover_stopwords(tokens)
    assert "dor" in remover_stopwords(tokens)


def teste_normalizar_reduz_flexao():
    # palavras da mesma família compartilham o mesmo radical (stem)
    assert normalizar("dores") == normalizar("dor")
    assert normalizar("palpitações") == normalizar("palpitação")


def teste_pipeline_completo():
    tokens = preprocessar("Dor no peito e falta de ar há 2 dias")
    # stopwords ("no", "e", "de", "há") removidas; conteúdo preservado
    assert "dor" in tokens
    assert "no" not in tokens
    assert "de" not in tokens
    assert all(t for t in tokens), "não deve haver tokens vazios"


def teste_pipeline_texto_vazio():
    assert preprocessar("") == []


def main():
    testes = [v for k, v in globals().items() if k.startswith("teste_")]
    for t in testes:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(testes)} testes de pré-processamento passaram.")


if __name__ == "__main__":
    main()

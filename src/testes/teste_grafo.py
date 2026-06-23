"""
Testes da estrutura de dados Grafo (issue #3).

Execução: python -m src.testes.teste_grafo
"""

from src.grafo import Grafo


def teste_adicionar_vertice_e_tipo():
    g = Grafo()
    g.adicionar_vertice("Q01", "documento")
    g.adicionar_vertice("dor", "termo")
    g.adicionar_vertice("Cardiologia", "categoria")

    assert g.quantidade_vertices() == 3
    assert g.get_tipo("Q01") == "documento"
    assert g.possui_vertice("dor")
    assert not g.possui_vertice("inexistente")


def teste_vertice_duplicado_nao_sobrescreve():
    g = Grafo()
    g.adicionar_vertice("Q01", "documento")
    g.adicionar_vertice("Q01", "documento")  # idempotente
    assert g.quantidade_vertices() == 1


def teste_tipo_invalido_levanta_erro():
    g = Grafo()
    try:
        g.adicionar_vertice("x", "invalido")
    except ValueError:
        return
    raise AssertionError("esperava ValueError para tipo inválido")


def teste_aresta_bidirecional_e_ponderada():
    g = Grafo()
    g.adicionar_vertice("Q01", "documento")
    g.adicionar_vertice("dor", "termo")
    g.adicionar_aresta("Q01", "dor", 3.0)

    assert g.get_vizinhos("Q01") == {"dor": 3.0}
    assert g.get_vizinhos("dor") == {"Q01": 3.0}
    assert g.quantidade_arestas() == 1


def teste_aresta_peso_invalido():
    g = Grafo()
    g.adicionar_vertice("a", "termo")
    g.adicionar_vertice("b", "termo")
    try:
        g.adicionar_aresta("a", "b", 0.0)
    except ValueError:
        return
    raise AssertionError("esperava ValueError para peso não-positivo")


def teste_aresta_vertice_inexistente():
    g = Grafo()
    g.adicionar_vertice("a", "termo")
    try:
        g.adicionar_aresta("a", "fantasma", 1.0)
    except ValueError:
        return
    raise AssertionError("esperava ValueError para vértice inexistente")


def teste_vertices_por_tipo():
    g = Grafo()
    g.adicionar_vertice("Q01", "documento")
    g.adicionar_vertice("dor", "termo")
    g.adicionar_vertice("Cardiologia", "categoria")

    assert g.get_vertices_por_tipo("documento") == ["Q01"]
    assert g.get_vertices_por_tipo("termo") == ["dor"]
    assert g.get_vertices_por_tipo("categoria") == ["Cardiologia"]


def main():
    testes = [v for k, v in globals().items() if k.startswith("teste_")]
    for t in testes:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(testes)} testes do Grafo passaram.")


if __name__ == "__main__":
    main()

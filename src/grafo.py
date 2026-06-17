"""
Estrutura de dados do grafo não-direcionado e ponderado.
Issue: #3
"""


class Grafo:
    def __init__(self):
        # { id: {"tipo": str, "vizinhos": {id: peso}} }
        self._vertices: dict[str, dict] = {}

    def adicionar_vertice(self, id: str, tipo: str) -> None:
        if id not in self._vertices:
            self._vertices[id] = {"tipo": tipo, "vizinhos": {}}

    def adicionar_aresta(self, u: str, v: str, peso: float) -> None:
        self._vertices[u]["vizinhos"][v] = peso
        self._vertices[v]["vizinhos"][u] = peso

    def get_vizinhos(self, u: str) -> dict[str, float]:
        return self._vertices[u]["vizinhos"]

    def get_vertices_por_tipo(self, tipo: str) -> list[str]:
        return [id for id, dados in self._vertices.items() if dados["tipo"] == tipo]

    def __repr__(self) -> str:
        contagem = {}
        for dados in self._vertices.values():
            t = dados["tipo"]
            contagem[t] = contagem.get(t, 0) + 1
        total_arestas = sum(
            len(d["vizinhos"]) for d in self._vertices.values()
        ) // 2
        return f"Grafo({contagem}, arestas={total_arestas})"

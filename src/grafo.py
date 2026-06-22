"""
Estrutura de dados do grafo não-direcionado e ponderado.
Issue: #3
"""


class Grafo:
    TIPOS_VALIDOS = {"documento", "termo", "categoria"}

    def __init__(self):
        # { id: {"tipo": str, "vizinhos": {id: peso}} }
        self._vertices: dict[str, dict] = {}





    def adicionar_vertice(self, id: str, tipo: str) -> None:
        """
        Adiciona vértice

        Args:
            id: Identificador do vértice
            tipo: documento ou termo ou categoria
        """
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo inválido: {tipo}. "
                f"Tipos permitidos: {self.TIPOS_VALIDOS}"
            )

        if id not in self._vertices:
            self._vertices[id] = {
                "tipo": tipo,
                "vizinhos": {}
            }






    def adicionar_aresta(self, u: str, v: str, peso: float) -> None:
        """
        Adiciona uma aresta bidirecional

        Args:
            u: vértice origem
            v: vértice destino
            peso: peso da aresta
        """
        if u not in self._vertices:
            raise ValueError(f"Vértice '{u}' não existe")

        if v not in self._vertices:
            raise ValueError(f"Vértice '{v}' não existe")

        if peso <= 0:
            raise ValueError("O peso deve ser positivo")

        self._vertices[u]["vizinhos"][v] = peso
        self._vertices[v]["vizinhos"][u] = peso

    def get_vizinhos(self, u: str) -> dict[str, float]:
        """
        Retorna os vizinhos de um vértice
        """
        if u not in self._vertices:
            raise ValueError(f"Vértice '{u}' não existe")

        return self._vertices[u]["vizinhos"]
    






    def get_vertices_por_tipo(self, tipo: str) -> list[str]:
        """
        Retorna todos os vértices de um tipo
        """
        return [
            id
            for id, dados in self._vertices.items()
            if dados["tipo"] == tipo
        ]
    






    def possui_vertice(self, id: str) -> bool:
        """
        Verifica se um vértice existe
        """
        return id in self._vertices
    






    def get_tipo(self, id: str) -> str:
        """
        Retorna o tipo de um vértice
        """
        if id not in self._vertices:
            raise ValueError(f"Vértice '{id}' não existe")

        return self._vertices[id]["tipo"]
    





    def quantidade_vertices(self) -> int:
        """
        Retorna o número  de vértices
        """
        return len(self._vertices)
    




    def quantidade_arestas(self) -> int:
        """
        Retorna o número de arestas
        """
        return (
            sum(
                len(dados["vizinhos"])
                for dados in self._vertices.values()
            )
            // 2
        )
    



    def __repr__(self) -> str:
        docs = len(self.get_vertices_por_tipo("documento"))
        termos = len(self.get_vertices_por_tipo("termo"))
        categorias = len(self.get_vertices_por_tipo("categoria"))

        return (
            f"Grafo("
            f"vertices={self.quantidade_vertices()}, "
            f"arestas={self.quantidade_arestas()}, "
            f"documentos={docs}, "
            f"termos={termos}, "
            f"categorias={categorias}"
            f")"
        )
    
    
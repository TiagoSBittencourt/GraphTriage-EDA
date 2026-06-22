import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from grafo import Grafo
g = Grafo()

# adicionando vértices
g.adicionar_vertice("Q01", "documento")
g.adicionar_vertice("dor", "termo")
g.adicionar_vertice("Cardiologia", "categoria")

# adicionando arestas
g.adicionar_aresta("Q01", "dor", 3.0)
g.adicionar_aresta("dor", "Cardiologia", 2.0)

print("Resumo:")
print(g)

print("\nVizinhos de Q01:")
print(g.get_vizinhos("Q01"))

print("\nVizinhos de dor:")
print(g.get_vizinhos("dor"))

print("\nDocumentos:")
print(g.get_vertices_por_tipo("documento"))

print("\nTermos:")
print(g.get_vertices_por_tipo("termo"))

print("\nCategorias:")
print(g.get_vertices_por_tipo("categoria"))
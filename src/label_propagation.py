"""
Algoritmo de Label Propagation implementado do zero.
Issue: #6
"""

from .grafo import Grafo


class LabelPropagation:
    def __init__(self):
        self.scores: dict[str, dict[str, float]] = {}
        self.historico: list[dict[str, dict[str, float]]] = []
        self._fixos: set[str] = set()

    def fit(
        self,
        grafo: Grafo,
        rotulos: dict[str, str],
        max_iter: int = 100,
        epsilon: float = 1e-4,
    ) -> None:
        # Inicialização
        for v in grafo.get_vertices_por_tipo("categoria"):
            self.scores[v] = {v: 1.0}
            self._fixos.add(v)

        for doc_id, cat in rotulos.items():
            self.scores[doc_id] = {cat: 1.0}
            self._fixos.add(doc_id)

        for v in grafo.get_vertices_por_tipo("documento") + grafo.get_vertices_por_tipo("termo"):
            if v not in self.scores:
                self.scores[v] = {}

        self.historico.append({v: dict(s) for v, s in self.scores.items()})

        for iteracao in range(max_iter):
            novos_scores: dict[str, dict[str, float]] = {}
            variacao_max = 0.0

            for v in list(self.scores.keys()):
                if v in self._fixos:
                    novos_scores[v] = self.scores[v]
                    continue

                vizinhos = grafo.get_vizinhos(v)
                peso_total = sum(vizinhos.values())
                if peso_total == 0:
                    novos_scores[v] = {}
                    continue

                acumulado: dict[str, float] = {}
                for u, peso in vizinhos.items():
                    for cat, score in self.scores.get(u, {}).items():
                        acumulado[cat] = acumulado.get(cat, 0.0) + peso * score

                novos_scores[v] = {cat: s / peso_total for cat, s in acumulado.items()}

                for cat, s in novos_scores[v].items():
                    diff = abs(s - self.scores[v].get(cat, 0.0))
                    variacao_max = max(variacao_max, diff)

            self.scores = novos_scores
            self.historico.append({v: dict(s) for v, s in self.scores.items()})

            if variacao_max < epsilon:
                print(f"Convergiu em {iteracao + 1} iterações.")
                return

        print(f"Atingiu max_iter={max_iter} sem convergir.")

    def predict(self, doc_id: str) -> tuple[str, float]:
        scores_doc = self.scores.get(doc_id, {})
        if not scores_doc:
            return ("indefinido", 0.0)
        melhor_cat = max(scores_doc, key=scores_doc.__getitem__)
        return (melhor_cat, round(scores_doc[melhor_cat], 4))

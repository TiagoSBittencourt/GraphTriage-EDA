"""
Índice invertido e contagem de co-ocorrência por categoria.
Issue: #4
"""

import math

from .preprocessamento import preprocessar


class IndiceInvertido:
    def __init__(self):
        # termo → { doc_id: frequência }
        self._indice: dict[str, dict[str, int]] = {}
        # nº total de documentos indexados (para o cálculo do IDF)
        self._n_documentos: int = 0

    def construir(self, documentos: list[dict]) -> None:
        self._n_documentos = len(documentos)
        for doc in documentos:
            tokens = preprocessar(doc["texto"])
            for token in tokens:
                if token not in self._indice:
                    self._indice[token] = {}
                self._indice[token][doc["id"]] = (
                    self._indice[token].get(doc["id"], 0) + 1
                )

    def get_docs(self, termo: str) -> list[str]:
        return list(self._indice.get(termo, {}).keys())

    def frequencia_no_doc(self, termo: str, doc_id: str) -> int:
        return self._indice.get(termo, {}).get(doc_id, 0)

    def frequencia_documento(self, termo: str) -> int:
        """Nº de documentos distintos que contêm o termo (document frequency)."""
        return len(self._indice.get(termo, {}))

    def idf(self, termo: str) -> float:
        """
        Inverse Document Frequency suavizado.

        Termos genéricos (ex.: "dor"), presentes em muitos documentos de várias
        categorias, recebem IDF baixo; termos discriminativos (ex.: "palpit")
        recebem IDF alto. Usado para ponderar as arestas Termo↔Categoria.
        """
        df = self.frequencia_documento(termo)
        return math.log((self._n_documentos + 1) / (df + 1)) + 1.0

    def contagem_por_categoria(
        self, termo: str, rotulos: dict[str, str]
    ) -> dict[str, int]:
        contagem: dict[str, int] = {}
        for doc_id in self.get_docs(termo):
            cat = rotulos.get(doc_id)
            if cat:
                contagem[cat] = contagem.get(cat, 0) + 1
        return contagem

    def termos(self) -> list[str]:
        return list(self._indice.keys())

    def top_termos_por_categoria(
        self, rotulos: dict[str, str], n: int = 10
    ) -> dict[str, list[tuple[str, int]]]:
        por_cat: dict[str, dict[str, int]] = {}
        for termo in self._indice:
            for cat, contagem in self.contagem_por_categoria(termo, rotulos).items():
                por_cat.setdefault(cat, {})[termo] = contagem
        return {
            cat: sorted(termos.items(), key=lambda x: x[1], reverse=True)[:n]
            for cat, termos in por_cat.items()
        }

    def imprimir_top_termos(self, rotulos: dict[str, str], n: int = 10) -> None:
        print(f"\n=== Top {n} termos por categoria ===")
        for cat, termos in self.top_termos_por_categoria(rotulos, n).items():
            print(f"\n  {cat}:")
            for termo, contagem in termos:
                print(f"    {termo:<20}: {contagem} doc(s)")

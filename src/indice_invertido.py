"""
Índice invertido e contagem de co-ocorrência por categoria.
Issue: #4
"""

from .preprocessamento import preprocessar


class IndiceInvertido:
    def __init__(self):
        # termo → { doc_id: frequência }
        self._indice: dict[str, dict[str, int]] = {}

    def construir(self, documentos: list[dict]) -> None:
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

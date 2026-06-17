"""
Módulo de pré-processamento de texto.
Issue: #2
"""

STOPWORDS = {
    "a", "ao", "aos", "as", "com", "da", "das", "de", "do", "dos",
    "e", "em", "há", "na", "nas", "no", "nos", "o", "os", "para",
    "por", "que", "se", "um", "uma", "após", "desde",
}

SUFIXOS = ["amento", "ção", "ções", "mente", "ando", "endo", "indo",
           "ado", "ido", "ar", "er", "ir", "dor", "dora"]


def _stemmer(token: str) -> str:
    for sufixo in sorted(SUFIXOS, key=len, reverse=True):
        if token.endswith(sufixo) and len(token) - len(sufixo) >= 3:
            return token[: -len(sufixo)]
    return token


def _tokenizar(texto: str) -> list[str]:
    import re
    return re.findall(r"[a-záéíóúâêîôûãõç]+|\d+", texto.lower())


def preprocessar(texto: str) -> list[str]:
    tokens = _tokenizar(texto)
    tokens = [t for t in tokens if t not in STOPWORDS]
    tokens = [_stemmer(t) for t in tokens]
    return tokens

import re

import snowballstemmer

from src.stopwords import STOPWORDS


# Stemmer oficial de Snowball para português (algoritmo de Porter para PT-BR).
# Resolve plurais e variações de flexão sem cortes ingênuos:
#   dores -> dor | palpitações -> palpit | manchas -> manch | após -> após
_STEMMER = snowballstemmer.stemmer("portuguese")


# -------------------------
# Tokenização
# -------------------------
def tokenizar(texto: str) -> list[str]:
    texto = texto.lower()
    return re.findall(r"\b\w+\b", texto)


# -------------------------
# Remoção de stopwords
# -------------------------
def remover_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOPWORDS]


# -------------------------
# Normalização (stemming de português via Snowball)
# -------------------------
def normalizar(token: str) -> str:
    return _STEMMER.stemWord(token)


# -------------------------
# Pipeline principal
# -------------------------
def preprocessar(texto: str) -> list[str]:
    tokens = tokenizar(texto)
    tokens = remover_stopwords(tokens)
    tokens = [normalizar(t) for t in tokens]
    return [t for t in tokens if t]

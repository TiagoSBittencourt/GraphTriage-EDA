import re
from src.stopwords import STOPWORDS


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
# Normalização leve (segura para dataset médico)
# -------------------------
def normalizar(token: str) -> str:
    if len(token) <= 3:
        return token

    # plural leve (conservador)
    if token.endswith("es") and len(token) > 4:
        return token[:-2]
    if token.endswith("s") and len(token) > 3:
        return token[:-1]

    return token


# -------------------------
# Pipeline principal
# -------------------------
def preprocessar(texto: str) -> list[str]:
    tokens = tokenizar(texto)
    tokens = remover_stopwords(tokens)
    tokens = [normalizar(t) for t in tokens]
    return tokens
import re
from src.stopwords import STOPWORDS


# -------------------------
# Tokenização
# -------------------------
def tokenizar(texto: str) -> list[str]:
    texto = texto.lower()
    return re.findall(r"\b\w+\b", texto)


# -------------------------
# Stopwords
# -------------------------
def remover_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOPWORDS]


# -------------------------
# Normalização leve (SEM stemming agressivo)
# -------------------------
def normalizar(token: str) -> str:
    # remove apenas plural simples com segurança

    if len(token) <= 3:
        return token

    # remove plural apenas se for seguro
    if token.endswith("s") and not token.endswith("es") and len(token) > 4:
        token = token[:-1]

    return token


# -------------------------
# Aplicar normalização
# -------------------------
def aplicar_normalizacao(tokens: list[str]) -> list[str]:
    return [normalizar(t) for t in tokens]


# -------------------------
# Pipeline principal
# -------------------------
def preprocessar(texto: str) -> list[str]:
    tokens = tokenizar(texto)
    tokens = remover_stopwords(tokens)
    tokens = aplicar_normalizacao(tokens)
    return tokens


# -------------------------
# Teste rápido opcional
# -------------------------
if __name__ == "__main__":
    exemplos = [
        "Dor no peito e falta de ar há 2 dias",
        "Paciente relata dores fortes no joelho esquerdo",
        "Apresenta náuseas e vômitos desde ontem",
        "Falta de ar e dor no peito ao caminhar",
        "Tontura e dor de cabeça persistente"
    ]

    for e in exemplos:
        print(e)
        print(preprocessar(e))
        print("-" * 40)
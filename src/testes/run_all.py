"""
Executa toda a suíte de testes do projeto.

Uso: python -m src.testes.run_all
"""

import importlib

MODULOS = [
    "src.testes.teste_grafo",
    "src.testes.teste_indice_invertido",
    "src.testes.teste_preprocessamento",
    "src.testes.teste_label_propagation",
    "src.testes.teste_avaliacao",
]


def main() -> int:
    falhas = 0
    for nome in MODULOS:
        mod = importlib.import_module(nome)
        print(f"\n### {nome} ###")
        try:
            mod.main()
        except AssertionError as e:
            falhas += 1
            print(f"  FALHOU: {e}")
        except Exception as e:  # noqa: BLE001
            falhas += 1
            print(f"  ERRO: {type(e).__name__}: {e}")

    print("\n" + "=" * 40)
    if falhas == 0:
        print("TODOS OS TESTES PASSARAM")
    else:
        print(f"{falhas} modulo(s) com falha")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())

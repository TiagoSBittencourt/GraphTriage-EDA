# GraphTriage-EDA

Sistema de triagem automática de queixas médicas usando classificação baseada em grafos com Label Propagation.

## Problema

Pacientes descrevem sintomas em texto livre (ex: *"dor no peito e falta de ar há 2 dias"*). O sistema classifica automaticamente a queixa na **especialidade médica** apropriada (Cardiologia, Ortopedia, Neurologia...) ou em **nível de urgência** (emergência, urgente, eletivo).

## Como funciona

### Pipeline

```
Queixas (texto livre)
  → Pré-processamento (tokenização, remoção de stopwords, stemming)
  → Cálculo TF-IDF + Índice invertido
  → Construção do grafo (vértices + arestas ponderadas)
  → Label Propagation (implementado do zero)
  → Categoria inferida + score de confiança
```

### Modelagem do Grafo

Grafo **não-direcionado, ponderado** com dois tipos de vértice:

| Vértice    | Representa                          |
|------------|-------------------------------------|
| Documento  | Uma queixa médica (texto)           |
| Categoria  | Especialidade médica alvo           |

| Aresta                   | Peso                                      |
|--------------------------|-------------------------------------------|
| Documento ↔ Documento    | Similaridade de cosseno (vetores TF-IDF)  |
| Documento ↔ Categoria    | 1.0 para documentos rotulados             |

Representação interna: **lista de adjacência** via dicionários Python.

### Algoritmo: Label Propagation

1. Documentos rotulados inicializam com score 1.0 na sua categoria
2. A cada iteração, vértices não-rotulados recebem a **média ponderada** dos scores dos vizinhos
3. Rótulos de documentos conhecidos permanecem fixos
4. Após convergência, o documento herda a categoria com maior score

**Complexidade:** O(iterações × arestas)

#### Exemplo

```
[Cardiologia]---Q1("dor no peito e falta de ar")---0.85---Q2("palpitação e tontura")
                 \
               0.6 \
                    Q5("dor no peito e inchaço no joelho")  → ???
               0.7 /
                 /
[Ortopedia]----Q3("dor no joelho ao caminhar")---0.9---Q4("fraturei o braço")
```

Q5 compartilha termos com Q1 (Cardiologia) e Q3 (Ortopedia). O Label Propagation resolve a ambiguidade via propagação transitiva pela estrutura do grafo.

## Estruturas de Dados

| Estrutura                           | Papel                                                         |
|-------------------------------------|---------------------------------------------------------------|
| Grafo (lista de adjacência / dict)  | Estrutura central — propagação de rótulos classifica textos   |
| Tabela hash (índice invertido)      | Construção eficiente das arestas + cálculo TF-IDF             |

## Análise e Avaliação

- Acurácia medida com holdout de documentos rotulados
- Visualização dos termos mais influentes por especialidade
- Propagação de rótulos visualizada iteração a iteração
- Discussão de casos ambíguos (ex: "dor de cabeça" → Neurologia ou urgência?)

## Dados

Queixas médicas fictícias geradas por LLM, com categorias claras e coerentes.

## Tech Stack

- **Python** — implementação do zero (sem bibliotecas de grafos)
- Processamento de texto: tokenização, stopwords, stemming
- Representação vetorial: TF-IDF (vetores esparsos)
- Similaridade: cosseno entre documentos

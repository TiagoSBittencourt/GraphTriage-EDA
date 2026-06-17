# GraphTriage-EDA

Sistema de triagem automática de queixas médicas usando classificação baseada em grafos com Label Propagation.

## Problema

Pacientes descrevem sintomas em texto livre (ex: *"dor no peito e falta de ar há 2 dias"*). O sistema classifica automaticamente a queixa na **especialidade médica** apropriada (Cardiologia, Ortopedia, Neurologia...) ou em **nível de urgência** (emergência, urgente, eletivo).

## Como funciona

### Pipeline

```
Queixas (texto livre)
  → Pré-processamento (tokenização, remoção de stopwords, stemming)
  → Índice invertido (termo → lista de documentos)
  → Construção do grafo (vértices + arestas ponderadas)
  → Label Propagation (implementado do zero)
  → Categoria inferida + score de confiança
```

### Modelagem do Grafo

Grafo **não-direcionado, ponderado** com três tipos de vértice:

| Vértice    | Representa                          |
|------------|-------------------------------------|
| Documento  | Uma queixa médica (texto)           |
| Termo      | Palavra-chave extraída das queixas  |
| Categoria  | Especialidade médica alvo           |

| Aresta                   | Peso                                                              |
|--------------------------|-------------------------------------------------------------------|
| Documento ↔ Termo        | Frequência do termo no documento                                  |
| Termo ↔ Categoria        | Nº de documentos daquela categoria que contêm o termo             |
| Documento ↔ Categoria    | 1.0 para documentos rotulados                                     |

Não há arestas diretas entre documentos — a conexão entre queixas acontece **indiretamente via os termos compartilhados**. Um termo muito frequente em documentos de Cardiologia terá aresta pesada com o vértice Cardiologia, influenciando documentos não rotulados que o contenham.

Representação interna: **lista de adjacência** via dicionários Python.

### Algoritmo: Label Propagation

1. Documentos rotulados inicializam com score 1.0 na sua categoria
2. A cada iteração, vértices não-rotulados recebem a **média ponderada** dos scores dos vizinhos
3. Rótulos de documentos conhecidos permanecem fixos
4. Após convergência, o documento herda a categoria com maior score

**Complexidade:** O(iterações × arestas)

#### Exemplo

```
[Cardiologia] ---2--- T("peito") ---1--- Q5("dor no peito e inchaço no joelho") → ???
[Ortopedia]   ---3--- T("joelho")---1---/
```

Q5 contém "peito" (presente em 2 docs de Cardiologia) e "joelho" (presente em 3 docs de Ortopedia). O Label Propagation decide a categoria pela força acumulada dos termos compartilhados.

## Estruturas de Dados

| Estrutura                           | Papel                                                                      |
|-------------------------------------|----------------------------------------------------------------------------|
| Grafo (lista de adjacência / dict)  | Estrutura central — propagação de rótulos classifica textos                |
| Tabela hash (índice invertido)      | Construção eficiente das arestas: mapeia termo → documentos que o contêm   |

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
- Índice invertido para contagem de co-ocorrência por categoria

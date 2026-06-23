<div align="center">

# 🩺 GraphTriage

**Triagem médica automática por classificação textual baseada em grafos.**

<img src="assets/logo.png" alt="GraphTriage Logo" width="200" style="border-radius: 20px;" />

<br />

Classifica queixas de pacientes em texto livre na **especialidade médica** correta
(Cardiologia · Ortopedia · Neurologia · Dermatologia · Gastroenterologia) usando um
**grafo tripartite** e **Label Propagation** — ambos implementados do zero, sem
bibliotecas de grafos ou de aprendizado de máquina.

<br />

[Problema](#1-definição-do-problema) • [Dados](#2-dados) • [Implementação](#3-implementação-da-solução) • [Algoritmos](#4-algoritmos-em-grafos-implementados-pelo-grupo) • [Como executar](#5-como-executar) • [Resultados](#7-análise-e-interpretação-dos-resultados) • [Visualizações](#8-visualizações)

</div>

---

> Trabalho da disciplina de Estruturas de Dados e Algoritmos (EDA).
> Tema do grupo: *implementar um sistema de classificação textual baseado em
> representações relacionais em grafos, modelando relações semânticas,
> estruturais ou estatísticas entre textos, palavras e categorias, e inferindo
> automaticamente a categoria de novos textos por meio de algoritmos de
> propagação/vizinhança no grafo.*

---

## 1. Definição do problema

Em prontos-socorros e plataformas de telemedicina, o paciente descreve seus
sintomas em **linguagem natural** — por exemplo:

> *"dor no peito e falta de ar, com leve dor lombar ao carregar peso"*

A **triagem** consiste em encaminhar essa queixa para a especialidade correta. É
um problema clássico de **Processamento de Linguagem Natural (PLN)**:
**classificação de texto curto**, com vocabulário informal, sinônimos e
**ambiguidade** (uma queixa pode citar sintomas de mais de uma especialidade).

**Objetivo:** dado um conjunto pequeno de queixas já rotuladas, inferir
automaticamente a especialidade de novas queixas **modelando as relações entre
documentos, palavras e categorias como um grafo** e propagando os rótulos
conhecidos pela estrutura. Ou seja, classificamos **sem** treinar um modelo
estatístico tradicional: a decisão emerge da topologia e dos pesos do grafo.

---

## 2. Dados

### Corpus

| Item                         | Valor                                            |
|------------------------------|--------------------------------------------------|
| Total de queixas             | **500**                                          |
| Categorias (especialidades)  | **5** (100 queixas cada)                          |
| Queixas rotuladas            | **400** (`Q001`–`Q400`, 80 por categoria)         |
| Queixas não rotuladas        | **100** (`U001`–`U100`, 20 por categoria)         |

As 5 categorias: **Cardiologia, Ortopedia, Neurologia, Dermatologia,
Gastroenterologia**.

### Organização

- [`data/corpus.json`](data/corpus.json) — todas as queixas. As rotuladas têm
  `categoria` preenchida; as ambíguas têm `categoria: ""` (entrada do
  classificador).
- [`data/corpus-rotulado.json`](data/corpus-rotulado.json) — **gabarito** das
  queixas `U*` (campo `categoria_real`), usado **apenas para avaliar** a
  propagação, nunca como entrada.
- [`data/dataset.md`](data/dataset.md) — documentação detalhada do corpus.

```json
{ "id": "Q001", "texto": "dor no peito e falta de ar há 2 dias", "categoria": "Cardiologia" }
{ "id": "U001", "texto": "dor no peito e falta de ar, com leve dor lombar ao carregar peso", "categoria": "" }
```

### Coerência dos dados gerados por LLM

As queixas são **fictícias, geradas com auxílio de LLM** (ver
[seção 10](#10-uso-de-llm)) e revisadas manualmente. Critérios de construção:

1. Linguagem natural de paciente, em português brasileiro.
2. Vocabulário **variado** dentro de cada categoria, para enriquecer o grafo.
3. Queixas **rotuladas** evitam sobreposição entre categorias (rótulos limpos).
4. Queixas **não rotuladas** misturam termos de 2–3 categorias, qualificando o
   sintoma secundário como *"leve"* para sinalizar a categoria dominante — um
   teste deliberado da capacidade do grafo de resolver ambiguidade pela força
   dos vizinhos.

---

## 3. Implementação da solução

### Pipeline

```
Queixas (texto livre)
  → 1. Pré-processamento     (tokenização · stopwords · stemming)
  → 2. Índice invertido      (termo → documentos · frequências · IDF)
  → 3. Construção do grafo   (vértices + arestas ponderadas)
  → 4. Label Propagation     (propagação iterativa de rótulos)
  → 5. Avaliação             (holdout · acurácia · matriz de confusão)
  → 6. Visualização          (grafo · evolução de scores · heatmap)
```

### Organização do código

```
GraphTriage-EDA/
├── main.py                       # orquestra a pipeline ponta a ponta
├── data/                         # corpus + gabarito + doc do dataset
├── docs/plots/                   # visualizações geradas
└── src/
    ├── preprocessamento.py       # (1) tokenização, stopwords, stemming
    ├── stopwords.py              # lista de stopwords PT-BR
    ├── indice_invertido.py       # (2) índice invertido + co-ocorrência + IDF
    ├── grafo.py                  # estrutura de dados Grafo (lista de adjacência)
    ├── construtor_grafo.py       # (3) monta o grafo tripartite
    ├── label_propagation.py      # (4) algoritmo de propagação (do zero)
    ├── avaliacao.py              # (5) holdout, acurácia, matriz de confusão
    ├── visualizacao.py           # (6) gráficos com matplotlib
    └── testes/                   # suíte de testes com asserções
```

Cada módulo tem responsabilidade única e é testável de forma isolada. O acoplamento
acontece por interfaces simples (listas de `dict`, o objeto `Grafo` e o objeto
`LabelPropagation`).

### Como as partes se completam

1. **Pré-processamento** ([`preprocessamento.py`](src/preprocessamento.py))
   converte cada texto em uma lista de **radicais** (stems). Ex.:
   `"dor no peito e falta de ar"` → `['dor', 'peit', 'falt', 'ar']`.
   Usa o stemmer **Snowball** para português, unificando flexões
   (`dores`/`dor`, `palpitações`/`palpit`) — sem isso, cada variação viraria um
   vértice diferente e o grafo perderia conexões.

2. **Índice invertido** ([`indice_invertido.py`](src/indice_invertido.py))
   mapeia `termo → {documento: frequência}`. É a **estrutura de dados adicional**
   do projeto (ver abaixo) e fornece, em tempo O(1), tudo que o construtor do
   grafo precisa: frequência de um termo num documento, documentos que contêm um
   termo, contagem por categoria e o **IDF**.

3. **Construtor do grafo** ([`construtor_grafo.py`](src/construtor_grafo.py))
   lê o índice e cria vértices e arestas ponderadas (ver
   [seção 3.2](#32-modelagem-do-grafo)).

4. **Label Propagation** ([`label_propagation.py`](src/label_propagation.py))
   propaga os rótulos conhecidos pelo grafo até convergir e prevê a categoria de
   cada queixa não rotulada.

5. **Avaliação** ([`avaliacao.py`](src/avaliacao.py)) e
   **visualização** ([`visualizacao.py`](src/visualizacao.py)) interpretam o
   resultado.

### 3.1 Estrutura de dados adicional (além do grafo)

Além do grafo, o sistema usa um **índice invertido**, implementado como uma
**tabela hash aninhada** (`dict` de `dict` em Python):

```python
{ "peit": {"Q001": 1, "Q002": 1, ...}, "joelh": {"Q123": 1, ...}, ... }
```

**Justificativa técnica.** A construção do grafo precisa responder repetidamente
a perguntas como *"em quantos documentos de Cardiologia o termo 'peito' aparece?"*.
Sem índice, cada pergunta exigiria varrer todos os documentos — O(D) por consulta.
O índice invertido responde em **tempo médio O(1)** por acesso (hash) e é a
estrutura canônica de PLN/recuperação de informação para esse fim. Ele também
centraliza o cálculo do **IDF** (frequência inversa de documento), usado para
ponderar as arestas. Assim, a complexidade da montagem do grafo cai de
O(D × T × D) para O(arestas).

### 3.2 Modelagem do grafo

Grafo **não-direcionado e ponderado**, **tripartite**, com três tipos de vértice:

| Vértice       | Representa                              |
|---------------|----------------------------------------|
| **Documento** | uma queixa médica (texto)              |
| **Termo**     | um radical (stem) extraído das queixas |
| **Categoria** | uma especialidade médica alvo          |

| Aresta                    | Peso                                                                        |
|---------------------------|-----------------------------------------------------------------------------|
| **Documento ↔ Termo**     | frequência do termo no documento                                            |
| **Termo ↔ Categoria**     | (nº de docs rotulados daquela categoria com o termo) **× IDF(termo)**        |
| **Documento ↔ Categoria** | `1.0`, apenas para documentos rotulados (ancora o rótulo)                    |

**Não há arestas diretas entre documentos.** Duas queixas se conectam
**indiretamente, pelos termos que compartilham**. É isso que permite classificar:
um termo frequente em documentos de Cardiologia ganha aresta pesada com o vértice
*Cardiologia* e, por propagação, "puxa" para Cardiologia qualquer queixa não
rotulada que o contenha.

**Por que o fator IDF?** Termos genéricos como *"dor"* aparecem em quase todas as
categorias (54 documentos só em Ortopedia, além de Cardiologia e Neurologia). Sem
correção, *"dor"* dominaria a propagação e empurraria tudo para a categoria mais
populosa. O **IDF** reduz o peso de termos espalhados e valoriza os
**discriminativos** (*"palpit"*, *"joelh"*, *"manch"*). Essa é a contribuição de
refinamento sobre a modelagem por co-ocorrência pura — ver
[seção 7](#7-análise-e-interpretação-dos-resultados).

**Representação interna:** **lista de adjacência** via dicionários
(`{id: {"tipo": str, "vizinhos": {id: peso}}}`). Escolhida porque o grafo é
**esparso** (cada queixa toca poucos termos): a lista de adjacência gasta O(V+E)
de memória e percorre vizinhos em O(grau), contra O(V²) de uma matriz de
adjacência.

Dimensões reais do grafo (corpus completo):

```
Vértices : 500 documentos | 443 termos | 5 categorias   (948 no total)
Arestas  : 2232 Documento↔Termo | 586 Termo↔Categoria | 320 Documento↔Categoria
```

---

## 4. Algoritmos em grafos (implementados pelo grupo)

### Label Propagation — implementado do zero

Algoritmo semi-supervisionado que propaga os rótulos conhecidos pela estrutura do
grafo:

1. **Inicialização.** Cada vértice de **categoria** recebe score `1.0` na própria
   categoria; cada **documento rotulado** recebe `1.0` na sua categoria. Esses
   vértices ficam **fixos** (nunca mudam). Termos e documentos não rotulados
   começam sem score.
2. **Propagação.** A cada iteração, todo vértice **não-fixo** recebe a **média
   ponderada** dos scores dos vizinhos:

   ```
   score(v, c) = Σ_u  peso(v,u) · score(u, c)  /  Σ_u peso(v,u)
   ```

3. **Convergência.** Repete até a maior variação de score ficar abaixo de
   `epsilon` (1e-4) ou atingir `max_iter`. No corpus completo, **converge em ~46
   iterações**.
4. **Predição.** Cada documento não rotulado herda a categoria de **maior score**;
   o valor do score é a **confiança**.

A propagação é em **dois saltos**: `categoria → termo → documento`. O score
"viaja" do vértice-categoria para os termos discriminativos e destes para as
queixas que os contêm.

**Complexidade:** O(iterações × arestas) — cada iteração visita cada aresta uma
vez.

#### Exemplo conceitual

```
[Cardiologia] --(peso alto)-- T("peit") --(1)-- U010("dor no peito e leve dor no joelho") --(1)-- T("joelh") --(peso menor)-- [Ortopedia]
```

`U010` cita *"peito"* (forte em Cardiologia) e *"joelho"* (forte em Ortopedia). O
Label Propagation acumula a força de cada caminho e decide pela **categoria
dominante** — neste caso, Cardiologia.

### Demais algoritmos próprios

- **Construção/percurso do grafo** (vizinhança, agrupamento por tipo, contagem de
  arestas) — [`grafo.py`](src/grafo.py).
- **Ranqueamento de termos por categoria** (`top_termos_por_categoria`) — ordena
  termos pela co-ocorrência, base das visualizações e da interpretação.

Nenhuma biblioteca de grafos (NetworkX, igraph) ou de ML (scikit-learn) é usada.
`matplotlib` aparece **somente** para desenhar os gráficos; `snowballstemmer`
**somente** para o stemming.

---

## 5. Como executar

```bash
# 1. ambiente
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. pipeline completa (classificação + avaliação + gráficos)
python main.py

# 3. suíte de testes
python -m src.testes.run_all
```

Os gráficos são salvos em [`docs/plots/`](docs/plots/).

---

## 6. Exemplos de entrada e saída

**Entrada** (queixa não rotulada, em `corpus.json`):

```json
{ "id": "U041", "texto": "dor de cabeça forte e visão embaçada, com leve náusea", "categoria": "" }
```

**Saída** (trecho do `python main.py`):

```
=== Classificação de queixas não rotuladas ===
  U041: Neurologia (score=0.46) | real: Neurologia ✓
  ...
```

**Relatório de avaliação:**

```
############ HOLDOUT (documentos rotulados) ############
Acurácia geral: 86.2%

Por categoria:
  Cardiologia         : 81.2%
  Ortopedia           : 100.0%
  ...

Matriz de confusão:
                   Cardiologia  Dermatologia  ...  Neurologia  Ortopedia
  Cardiologia               13             0  ...           2          1
  ...
```

---

## 7. Análise e interpretação dos resultados

### Acurácia

| Conjunto                              | Acurácia |
|---------------------------------------|----------|
| **Holdout** (20% das rotuladas)       | **86,2%**|
| **Queixas ambíguas** `U*` (gabarito)  | **87,0%**|

Com 5 classes balanceadas, o acaso seria **20%**. A acurácia validada por holdout
é **estável entre 84% e 90%** ao variar a semente aleatória, indicando que o
resultado não depende de uma partição sortuda.

### Efeito do refinamento por IDF

| Modelagem das arestas Termo↔Categoria | Holdout | Ambíguas |
|---------------------------------------|---------|----------|
| Co-ocorrência pura                    | 83,8%   | 87,0%    |
| **Co-ocorrência × IDF** (adotado)     | **86,2%** | **87,0%** |

Ponderar pelo IDF melhora o holdout sem prejudicar as ambíguas: ao reduzir o peso
de *"dor"* (presente em 3 das 5 especialidades), o modelo passa a decidir pelos
termos realmente discriminativos.

### Padrões observados nos termos por categoria

O ranqueamento de termos revela "assinaturas" coerentes por especialidade:

- **Cardiologia:** `peit`, `falt(a) ar`, `palpit`, `suor`, `coraçã`
- **Neurologia:** `cabec`, `tremor`, `formig`, `dormênc`, `tontur`
- **Ortopedia:** `joelh`, `ombro`, `tornozel`, `quadril`, `inchac`

São exatamente os sintomas que um clínico associaria a cada área — evidência de
que o grafo capturou relações semânticas reais, não ruído.

### Onde o modelo erra (e por quê)

Os **erros mais confiantes** concentram-se em fronteiras clinicamente ambíguas:

- **Neurologia ↔ Cardiologia:** *tontura*, *suor* e *formigamento* ocorrem nas
  duas (ex.: pré-síncope cardíaca vs. neurológica).
- **Ortopedia ↔ outras:** *"dor"* sozinho é pouco informativo; quando a queixa
  ortopédica não traz o termo da região (joelho, ombro), a propagação hesita.

Esses erros são **interpretáveis e esperados** — refletem sobreposição real de
vocabulário, não falha de implementação. As visualizações
([seção 8](#8-visualizações)) tornam esse comportamento explícito.

---

## 8. Visualizações

Geradas por [`visualizacao.py`](src/visualizacao.py) e salvas em `docs/plots/`:

| Gráfico                                                 | O que mostra                                                            |
|---------------------------------------------------------|-------------------------------------------------------------------------|
| [`grafo.png`](docs/plots/grafo.png)                     | grafo tripartite (categorias, top termos e documentos) com pesos das arestas |
| [`evolucao_scores.png`](docs/plots/evolucao_scores.png) | scores de um documento ao longo das iterações até convergir            |
| [`heatmap_scores.png`](docs/plots/heatmap_scores.png)   | scores finais das queixas `U*` por categoria, com a predição destacada |

> A descrição detalhada de cada gráfico e as conclusões extraídas estão em
> **[`docs/plots/README.md`](docs/plots/README.md)**.

---

## 9. Testes

A suíte cobre os cinco módulos do núcleo com **asserções** (não apenas
demonstrações):

```bash
python -m src.testes.run_all
```

Cobertura: estrutura do grafo, índice invertido (incl. IDF e co-ocorrência),
pré-processamento, convergência/predição do Label Propagation e métricas de
avaliação.

---

## 10. Uso de LLM

- **Geração do corpus.** As 500 queixas fictícias foram geradas com auxílio de um
  LLM, a partir de instruções que fixaram as categorias, o estilo de fala do
  paciente, a variação de vocabulário e o desenho das ambiguidades. Todas as
  queixas foram revisadas manualmente quanto à coerência clínica.
- **Apoio ao desenvolvimento.** LLM foi usado como apoio em revisão de código e
  documentação. **Os algoritmos centrais — grafo, índice invertido e Label
  Propagation — foram implementados pelo grupo, sem bibliotecas prontas.**

---

## 11. Equipe e contribuições

| Integrante                | Contribuição principal                                                     |
|---------------------------|-----------------------------------------------------------------------------|
| **Tiago Bittencourt**     | corpus/dataset, índice invertido, construção do grafo, Label Propagation, pipeline e refinamento de acurácia (IDF) |
| **Bernardo Broetto Brun** | módulo de pré-processamento (tokenização, stopwords, stemming) e estrutura de dados Grafo |
| **João Carvalho**         | módulo de avaliação e métricas (holdout, acurácia, matriz de confusão)     |
| **Cadu Motta**            | visualizações do grafo e da propagação (matplotlib)                        |

> Mapeamento derivado do histórico do repositório (issues #1–#8). Ajuste conforme
> a divisão final do grupo, se necessário.

---

## 12. Stack técnica

- **Python 3.10+** — núcleo (grafo, índice, Label Propagation) implementado do zero.
- **snowballstemmer** — stemming em português.
- **matplotlib** — visualizações.

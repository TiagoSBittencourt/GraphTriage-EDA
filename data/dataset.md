# Dataset — Queixas Médicas para GraphTriage

## Categorias Médicas

| # | Categoria          | Descrição                                                    |
|---|--------------------|--------------------------------------------------------------|
| 1 | **Cardiologia**    | Doenças do coração e sistema circulatório                    |
| 2 | **Ortopedia**      | Lesões e doenças do sistema musculoesquelético               |
| 3 | **Neurologia**     | Distúrbios do sistema nervoso central e periférico           |
| 4 | **Dermatologia**   | Doenças e condições da pele, cabelo e unhas                  |
| 5 | **Gastroenterologia** | Doenças do trato digestivo e órgãos associados            |

## Estatísticas do Corpus

- **500 queixas no total** (100 por categoria)
- **400 queixas rotuladas** (`Q001`–`Q400`, 80 por categoria)
- **100 queixas não rotuladas** (`U001`–`U100`, 20 por categoria) — para classificação via Label Propagation
- Os rótulos reais das queixas não rotuladas (usados para avaliar a propagação) estão em `corpus-rotulado.json`

### Distribuição das queixas não rotuladas (gabarito)

| Faixa de IDs | Categoria real     |
|--------------|--------------------|
| U001–U020    | Cardiologia        |
| U021–U040    | Ortopedia          |
| U041–U060    | Neurologia         |
| U061–U080    | Dermatologia       |
| U081–U100    | Gastroenterologia  |

## Queixas Ambíguas

As 100 queixas não rotuladas (`U001`–`U100`) foram desenhadas para conter termos de mais de uma categoria, testando a capacidade do Label Propagation de resolver ambiguidades pela força dos vizinhos no grafo. Cada uma combina o(s) sintoma(s) **dominante(s)** de uma categoria com um sintoma **secundário de outra categoria, qualificado como "leve"**, sinalizando qual deve prevalecer. A categoria real (a dominante) está registrada em `corpus-rotulado.json`.

Exemplos:

- `U001` — "dor no peito e falta de ar, com **leve** dor lombar ao carregar peso" → dominante **Cardiologia** (sintomas cardíacos), secundário leve de Ortopedia.
- `U041` — "dor de cabeça forte e visão embaçada, com **leve** náusea" → dominante **Neurologia**, secundário leve de Gastroenterologia.
- `U061` — "manchas vermelhas e coceira na pele, com **leve** náusea após comer" → dominante **Dermatologia**, secundário leve de Gastroenterologia.

## Critérios de Construção

1. Cada queixa usa linguagem natural em português brasileiro, simulando fala de paciente
2. Termos foram variados dentro de cada categoria para enriquecer o vocabulário do grafo
3. Queixas rotuladas evitam sobreposição excessiva entre categorias para manter rótulos limpos
4. Queixas não rotuladas deliberadamente misturam termos de 2–3 categorias, geralmente qualificando o termo da categoria secundária como "leve" para sinalizar qual deve prevalecer
5. A categoria real de cada queixa não rotulada é mantida separadamente em `corpus-rotulado.json`, permitindo avaliar a acurácia do Label Propagation sem expor o rótulo no corpus de entrada

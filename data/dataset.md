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

- **80 queixas rotuladas** (16 por categoria)
- **20 queixas não rotuladas** (para classificação via Label Propagation)
- **100 queixas no total**
- Os rótulos reais das queixas não rotuladas (usados para avaliar a propagação) estão em `corpus-rotulado.json`

## Queixas Ambíguas Documentadas

As queixas não rotuladas (U001–U020) foram intencionalmente desenhadas para conter termos de múltiplas categorias, testando a capacidade do Label Propagation de resolver ambiguidades pela força dos vizinhos no grafo. A categoria real de cada uma está registrada em `corpus-rotulado.json`.

### U001 — "dor de cabeça forte com náusea e visão embaçada"
- **Neurologia**: "dor de cabeça", "visão embaçada" são sintomas clássicos neurológicos (enxaqueca com aura)
- **Gastroenterologia**: "náusea" aparece frequentemente em queixas gástricas
- **Categoria real: Neurologia** — mais termos neurológicos que gástricos

### U002 — "tontura forte com palpitações e suor frio"
- **Cardiologia**: "palpitações" e "suor frio" são termos cardíacos
- **Neurologia**: "tontura" aparece em queixas neurológicas
- **Categoria real: Cardiologia** — 2 termos cardíacos vs 1 neurológico

### U003 — "inchaço no joelho e manchas roxas na pele"
- **Ortopedia**: "inchaço no joelho" é termo ortopédico clássico
- **Dermatologia**: "manchas roxas na pele" sugere condição dermatológica
- **Categoria real: Ortopedia**

### U004 — "dormência nas mãos e dor na coluna cervical"
- **Neurologia**: "dormência" é sintoma neurológico (neuropatia)
- **Ortopedia**: "dor na coluna cervical" é queixa ortopédica
- **Categoria real: Neurologia** — cervicobraquialgia tem componente de ambas, mas o termo neurológico prevalece

### U005 — "dor no peito constante que piora com esforço leve e leve dor lombar ao carregar peso"
- **Cardiologia**: "dor no peito" e "esforço leve" são indicadores cardíacos
- **Ortopedia**: "dor lombar ao carregar peso" é queixa ortopédica, mas qualificada como "leve"
- **Categoria real: Cardiologia** — o termo cardíaco é o foco central da queixa

### U006 — "palpitações e vermelhidão na pele após uso de novo medicamento"
- **Cardiologia**: "palpitações" é termo cardíaco
- **Dermatologia**: "vermelhidão na pele após medicamento" sugere reação cutânea
- **Categoria real: Dermatologia** — reação alérgica/dermatológica ao medicamento

### U007 — "dor no peito intensa após refeições com sensação de queimação"
- **Cardiologia**: "dor no peito intensa" é forte indicador cardíaco
- **Gastroenterologia**: "após refeições" e "sensação de queimação" apontam para refluxo/azia
- **Categoria real: Gastroenterologia**

### U008 — "dor abdominal forte que piora ao se curvar e dor na coluna lombar"
- **Gastroenterologia**: "dor abdominal forte" é termo central da gastro
- **Ortopedia**: "piora ao se curvar" e "dor na coluna lombar" são termos ortopédicos
- **Categoria real: Ortopedia**

### U009 — "formigamento e coceira intensa na pele do braço"
- **Neurologia**: "formigamento" é sintoma neurológico
- **Dermatologia**: "coceira intensa na pele" é sintoma dermatológico
- **Categoria real: Dermatologia**

### U010 — "pele e olhos amarelados com manchas vermelhas pelo corpo"
- **Gastroenterologia**: "pele e olhos amarelados" é sinal clássico de icterícia (causa hepática/gástrica)
- **Dermatologia**: "manchas vermelhas pelo corpo" sugere condição cutânea
- **Categoria real: Gastroenterologia**

### U011 — "tontura forte, náusea e palpitações após o almoço"
- **Cardiologia/Neurologia**: "tontura" e "palpitações" cruzam essas categorias
- **Gastroenterologia**: "náusea... após o almoço" associa o quadro à digestão
- **Categoria real: Gastroenterologia** — o contexto pós-refeição direciona a causa

### U012 — "dor no peito, formigamento no braço esquerdo e dor na coluna cervical"
- **Cardiologia**: "dor no peito" e "formigamento no braço esquerdo" são indicadores cardíacos clássicos
- **Neurologia**: "formigamento" isoladamente também é sintoma neurológico
- **Ortopedia**: "dor na coluna cervical" é queixa ortopédica
- **Categoria real: Cardiologia** — ambiguidade tripla resolvida a favor do quadro cardíaco

### U013 — "dor abdominal intensa após refeições, manchas na pele e leve dor lombar"
- **Gastroenterologia**: "dor abdominal... após refeições" é o termo central
- **Dermatologia**: "manchas na pele"
- **Ortopedia**: "leve dor lombar" (qualificada como leve)
- **Categoria real: Gastroenterologia**

### U014 — "dor de cabeça leve, manchas vermelhas que coçam na pele e vômitos ocasionais"
- **Neurologia**: "dor de cabeça" (qualificada como leve)
- **Dermatologia**: "manchas vermelhas que coçam na pele" é o termo dominante
- **Gastroenterologia**: "vômitos ocasionais"
- **Categoria real: Dermatologia**

### U015 — "suor frio, tremores nas mãos em repouso e pele pálida"
- **Cardiologia**: "suor frio" é termo cardíaco
- **Neurologia**: "tremores nas mãos em repouso" e "pele pálida" reforçam o quadro neurológico
- **Categoria real: Neurologia**

### U016 — "dor lombar irradiando para a perna com formigamento e prisão de ventre"
- **Ortopedia**: "dor lombar irradiando para a perna" e "formigamento" são termos ortopédicos/neurológicos clássicos (ciatalgia)
- **Gastroenterologia**: "prisão de ventre"
- **Categoria real: Ortopedia**

### U017 — "dor no peito intensa, falta de ar e leve coceira no peito"
- **Cardiologia**: "dor no peito intensa" e "falta de ar" dominam a queixa
- **Dermatologia**: "leve coceira no peito" (qualificada como leve)
- **Categoria real: Cardiologia**

### U018 — "dor no joelho ao subir escadas e leve tontura ao se levantar rápido"
- **Ortopedia**: "dor no joelho ao subir escadas" é o termo dominante
- **Neurologia/Cardiologia**: "leve tontura ao se levantar rápido" (qualificada como leve)
- **Categoria real: Ortopedia**

### U019 — "urticária pelo corpo todo e leve náusea após comer camarão"
- **Dermatologia**: "urticária pelo corpo todo" é o termo dominante (reação alérgica cutânea)
- **Gastroenterologia**: "leve náusea após comer camarão" (qualificada como leve)
- **Categoria real: Dermatologia**

### U020 — "crises de tremores nas mãos, confusão mental e leve dor no punho"
- **Neurologia**: "tremores nas mãos" e "confusão mental" dominam a queixa
- **Ortopedia**: "leve dor no punho" (qualificada como leve)
- **Categoria real: Neurologia**

## Critérios de Construção

1. Cada queixa usa linguagem natural em português brasileiro, simulando fala de paciente
2. Termos foram variados dentro de cada categoria para enriquecer o vocabulário do grafo
3. Queixas rotuladas evitam sobreposição excessiva entre categorias para manter rótulos limpos
4. Queixas não rotuladas deliberadamente misturam termos de 2–3 categorias, geralmente qualificando o termo da categoria secundária como "leve" para sinalizar qual deve prevalecer
5. A categoria real de cada queixa não rotulada é mantida separadamente em `corpus-rotulado.json`, permitindo avaliar a acurácia do Label Propagation sem expor o rótulo no corpus de entrada

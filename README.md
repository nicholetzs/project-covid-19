# KDD & BI Dashboard: COVID-19 Microdados (ES)

<p align="center">
  <img src="https://img.shields.io/github/repo-size/nicholetzs/KDD?style=for-the-badge&color=gold" alt="Repo Size">
  <img src="https://img.shields.io/github/languages/top/nicholetzs/KDD?style=for-the-badge&color=blue" alt="Top Language">
  <img src="https://img.shields.io/github/last-commit/nicholetzs/KDD?style=for-the-badge&color=orange" alt="Last Commit">
</p>

> **Status do Projeto:** Em producao  
> **Dashboard online:** [Data Science - COVID-19 ES · Streamlit](https://xawpfum7gezaxhvqwlphtb.streamlit.app/)

---

## Visao Geral

Este projeto apresenta um dashboard interativo de Business Intelligence construido com `Streamlit`, `Pandas` e `Plotly Express` para explorar microdados de notificacoes de COVID-19 no Espirito Santo.

O foco do projeto e aplicar conceitos de `KDD (Knowledge Discovery in Databases)` sobre uma base tabular publica, transformando dados brutos em indicadores visuais que apoiam a interpretacao e a tomada de decisao baseada em dados.

---

## O que o dashboard mostra

O aplicativo exibe indicadores e visualizacoes sobre:

- total de registros carregados
- quantidade de municipios e variaveis
- top 10 municipios com maior numero de notificacoes
- colunas com maior volume de dados faltantes
- distribuicao por sexo
- distribuicao por faixa etaria
- sintomas mais frequentes
- comorbidades presentes em registros de obito
- evolucao temporal das notificacoes

---

## Stack Tecnologica

| Tecnologia         | Funcao                          |
| :----------------- | :------------------------------ |
| **Python 3.12**    | Linguagem principal             |
| **Pandas**         | Leitura, tratamento e agregacao |
| **Streamlit**      | Interface web do dashboard      |
| **Plotly Express** | Visualizacao interativa         |

---

## Como o projeto aplica KDD

Este repositorio representa principalmente as etapas abaixo:

1. **Selecao**  
   O projeto utiliza o arquivo `data/MICRODADOS_DIVERSIFICADO.csv` como base para analise.

2. **Pre-processamento**  
   Durante a carga, o app valida a existencia do arquivo, le o CSV com `pandas.read_csv(...)` e converte colunas textuais para `category` para reduzir uso de memoria.

3. **Transformacao**  
   Os dados sao organizados em formatos adequados para visualizacao, com operacoes como:
   - contagem por categoria com `value_counts()`
   - agrupamento temporal por mes com `groupby()`
   - filtragem de registros de obito para analise de comorbidades
   - calculo de nulos por coluna

4. **Interpretacao**  
   Os resultados sao apresentados em um dashboard com abas tematicas, permitindo comparar incidencia, perfil demografico, aspectos clinicos e comportamento temporal.

> Observacao: o codigo atual le integralmente o CSV presente neste repositorio. Nao ha, nesta versao, implementacao de amostragem por `head`, `middle` e `tail`.

---

## Estrutura do projeto

```text
KDD/
|-- app.py
|-- README.md
|-- requirements.txt
|-- data/
|   `-- MICRODADOS_DIVERSIFICADO.csv
`-- src/
    |-- carregarDados.py
    |-- topMunicipios.py
    |-- distribuicaoSexo.py
    |-- distribuicaoClassificacao.py
    |-- faixaEtaria.py
    |-- sintomas.py
    |-- comorbidade.py
    |-- evolucaoTemporal.py
    |-- calcularNulos.py
    `-- tabelaCruzada.py
```

---

## Como executar localmente

### 1. Clonar o repositorio

```bash
git clone https://github.com/nicholetzs/KDD.git
cd KDD
```

### 2. Instalar as dependencias

```bash
pip install -r requirements.txt
```

### 3. Iniciar o Streamlit

```bash
streamlit run app.py
```

---

## Observacoes sobre os dados

- O dashboard utiliza o CSV disponivel na pasta `data/`.
- As metricas exibidas dependem diretamente do conteudo desse arquivo.
- Se o CSV for substituido por uma versao maior ou mais recente, os resultados do dashboard mudarao automaticamente.

---

## Possiveis evolucoes

- incluir filtros interativos por municipio, periodo e classificacao
- adicionar analises comparativas entre confirmados, descartados e obitos
- documentar com mais profundidade os insights gerados pelo dashboard
- expandir a etapa de mineracao com segmentacoes, regras ou modelos preditivos

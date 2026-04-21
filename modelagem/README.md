# Por que modelar em estrela neste projeto

Este documento resume por que o dashboard de COVID-19 fica melhor para analise quando sai do CSV cru e passa para um modelo estrela.

## KDD sem modelagem (estado atual do app)

- O Streamlit le o CSV inteiro e faz transformações na hora de montar cada grafico.
- Regras de negocio (confirmado, obito, cura, latencias) ficam espalhadas no codigo da interface.
- Cada aba recalcula agregacoes parecidas, aumentando custo de CPU e tempo de resposta.
- Funciona bem para prototipo, mas cresce mal quando entram mais perguntas, filtros e historico.

## KDD com modelagem estrela

- A carga prepara antes os dados em `fato_notif_covid` + dimensoes (`tempo`, `localidade`, `perfil`, etc.).
- O Streamlit deixa de transformar dado bruto e passa a consultar estruturas prontas para analise.
- As regras de negocio ficam centralizadas no ETL, com definicao unica e reutilizavel.
- Consultas analiticas ficam mais rapidas porque agregam direto na fato com chaves inteiras e joins simples.

## Por que é mais performético na pratica

1. Menos trabalho por consulta: o custo pesado de limpeza e padronização sai do tempo de tela e vai para a carga.
2. Menos repetição: em vez de recalcular `groupby` e filtros em cada gráfico, as tabelas ja estao no formato analitico.
3. Joins previsiveis: fato-dimensao com SK inteira e mais barato do que reprocessar texto e datas toda vez.
4. Cache mais eficiente: o resultado de consulta dimensional varia menos que pipelines dinamicos no frontend.

## O que significa "inteligencia de transformacao"

Aqui, "inteligencia" e a logica que hoje esta no Streamlit para:

- padronizar valores textuais
- tratar nulos
- derivar flags (confirmado, obito, cura)
- calcular latencias entre datas
- construir faixas e classificacoes

No modelo estrela, essa inteligencia sai da interface e vai para o ETL/modelagem. O frontend fica mais simples: consultar, filtrar e visualizar.

## Regra de decisao para este projeto

- Se o objetivo for demonstracao rapida: CSV direto atende.
- Se o objetivo for BI evolutivo (mais indicadores, comparacoes historicas e confiabilidade): modelagem estrela compensa.

---

## Fase 1: Modelagem (DDL)

A modelagem é a definição das estruturas (tabelas, colunas, tipos, relacionamentos).

Arquivo: `modelagem/01_ddl_modelo_estrela.sql`

Este script cria 8 tabelas conforme seu esquema:
- 7 dimensões: tempo, localidade, perfil_paciente, classificacao, sintomas, comorbidade, teste
- 1 fato: notif_covid (grão = 1 notificação)

O esquema segue rigorosamente Kimball:
1. Surrogate keys (SK) em cada dimensão
2. Role-playing: 6 FKs de tempo na fato (notificação, cadastro, diagnóstico, coleta, encerramento, óbito)
3. Junk dimensions: sintomas e comorbidade consolidam flags booleanas
4. Known members: SK -1 = "Desconhecido" em toda dimensão (evita NULLs nas FKs)
5. Medidas na fato: qtd, flags (confirmado, obito, internado, cura), idade, latências

### Para executar (PostgreSQL):

```bash
psql -U postgres -d seu_banco -f modelagem/01_ddl_modelo_estrela.sql
```

**Resultado esperado:** 8 tabelas vazias (apenas estrutura), prontas para receber dados no próximo passo.

## Como comecar a modelagem agora

1. Execute o ETL de modelagem:

```bash
python modelagem/build_star_schema.py
```

2. O script gera os arquivos em `modelagem/output/`:
- `dim_tempo.csv`
- `dim_localidade.csv`
- `dim_perfil_paciente.csv`
- `dim_classificacao.csv`
- `dim_sintomas.csv`
- `dim_comorbidade.csv`
- `dim_teste.csv`
- `fato_notif_covid.csv`

3. Valide o grão da fato:
- quantidade de linhas da `fato_notif_covid` deve ser igual ao total de notificacoes do CSV de origem.

4. Valide integridade basica:
- nenhuma FK principal da fato deve ficar nula (`sk_local`, `sk_perfil`, `sk_class`, `sk_sint`, `sk_como`, `sk_teste`).

5. Se quiser levar para banco relacional, use o DDL em `modelagem/ddl_star_schema.sql`.

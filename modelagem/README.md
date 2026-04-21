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

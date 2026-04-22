apenas anotações

A primeira pasta do KDD é uma análise de dados simples, sem normalização ou limpeza de dados.. apenas extração de informações com visualização SEM MODELAGEM DOS DADOS no streamlit, o que tem suas implicações.

basicamente:

1. Dados brutos
CSV original, sujo e grande.

2. Camada analítica (modelagem)
Aqui você organiza os dados para responder perguntas de negócio rápido e com consistência.

3. Apresentação (Streamlit)
Só consome a camada analítica e desenha gráficos.

Caso eu pule a 2. e fosse fazer esses processos mais robsutos de ETL e análise de dados, o Streamlit vira ETL + BI + UI ao mesmo tempo, mais código complexo na interface, mais chance de regra inconsistente entre gráficos e pior manutenção quando o projeto cresce.

Poooréém, usando a modelagem antes, cada métrica já nasce padronizada, consultas ficam mais rápidas, o app fica simples de manter, trocar Streamlit por outra ferramenta no futuro fica fácil!
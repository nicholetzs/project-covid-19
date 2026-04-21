import streamlit as st
import plotly.express as px
import pandas as pd

# 1. Configuração de Layout
st.set_page_config(
    page_title="Data Science - COVID-19 ES",
    page_icon="🧬",
    layout="wide" 
)

# Importações
from src.carregarDados import carregar_dados
from src.calcularNulos import calcular_nulos
from src.distribuicaoClassificacao import distribuicao_classificacao
from src.topMunicipios import top_municipios
from src.distribuicaoSexo import distribuicao_sexo
from src.faixaEtaria import faixa_etaria
from src.sintomas import sintomas_frequentes
from src.comorbidade import comorbidades_obitos
from src.evolucaoTemporal import evolucao_temporal

# 2. Carga de Dados
@st.cache_data
def get_data():
    return carregar_dados()

df = get_data()

# 3. Cabeçalho Principal (Moderno)
st.title("🧬 Intelligence Dashboard | COVID-19")
st.markdown("---")

# 4. KPIs (Métricas de Topo) - Agora com cores visíveis
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total de Amostras", f"{len(df):,}")
with m2:
    st.metric("Municípios", df['Municipio'].nunique())
with m3:
    st.metric("Variáveis", len(df.columns))
with m4:
    st.metric("Engine", "Pandas/KDD")

st.write("") # Espaçamento

# 5. Navegação por TABS (Substituindo o select/radio da sidebar)
# Isso deixa o design muito mais "Dashboard de BI"
tab_geral, tab_demografico, tab_clinico, tab_temporal = st.tabs([
    "🔍 Visão Geral", 
    "👥 Perfil Demográfico", 
    "🏥 Análise Clínica", 
    "📅 Evolução Temporal"
])

# --- CONTEÚDO DAS TABS ---

with tab_geral:
    st.subheader("Análise de Ranking e Qualidade")
    col1, col2 = st.columns([1.2, 1]) # Proporção para não apertar o gráfico
    
    with col1:
        dados_mun = top_municipios(df)
        fig_mun = px.bar(
            dados_mun, x="Número de Notificações", y="Municipio", 
            orientation='h', color="Número de Notificações",
            color_continuous_scale="Viridis",
            title="Top 10 Municípios com Maior Incidência"
        )
        st.plotly_chart(fig_mun, use_container_width=True)
        
    with col2:
        nulos = calcular_nulos(df)
        fig_nulos = px.pie(nulos.head(10), names="Coluna", values="Quantidade", title="Top 10 Colunas com Dados Faltantes")
        st.plotly_chart(fig_nulos, use_container_width=True)

with tab_demografico:
    st.subheader("Perfil dos Notificados")
    c1, c2 = st.columns(2)
    
    with c1:
        sexo = distribuicao_sexo(df)
        fig_sexo = px.pie(sexo, names="Sexo", values="Frequência", hole=0.5, title="Distribuição por Gênero")
        st.plotly_chart(fig_sexo, use_container_width=True)
        
    with c2:
        faixa = faixa_etaria(df)
        fig_faixa = px.bar(faixa, x="FaixaEtaria", y="Quantidade", color="FaixaEtaria", title="Distribuição por Faixa Etária (Anos)")
        st.plotly_chart(fig_faixa, use_container_width=True)

with tab_clinico:
    st.subheader("Indicadores de Saúde")
    # Usando colunas para sintomas e comorbidades ficarem grandes
    col_sint, col_comorb = st.columns(2)
    
    with col_sint:
        sintomas = sintomas_frequentes(df)
        fig_sint = px.bar(sintomas, x="Sintoma", y="Quantidade", color="Sintoma", title="Sintomas Mais Relatados")
        st.plotly_chart(fig_sint, use_container_width=True)
        
    with col_comorb:
        comorb = comorbidades_obitos(df)
        fig_com = px.bar(comorb, x="Comorbidade", y="Quantidade", color="Comorbidade", title="Comorbidades Presentes em Óbitos")
        st.plotly_chart(fig_com, use_container_width=True)

with tab_temporal:
    st.subheader("Análise Cronológica")
    tempo = evolucao_temporal(df)
    # Gráfico de linha grande para ver bem a curva
    fig_tempo = px.line(
        tempo, x="AnoMes", y="Quantidade", 
        title="Curva de Notificações ao Longo do Tempo",
        markers=True
    )
    fig_tempo.update_traces(line_color='#FF4B4B')
    st.plotly_chart(fig_tempo, use_container_width=True)
import pandas as pd
import streamlit as st
import os

@st.cache_data
def carregar_dados():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    caminho = os.path.join(diretorio_atual, "..", "data", "MICRODADOS_DIVERSIFICADO.csv")
    
    # Correção de segurança: Se o '..' não funcionar (caso o script esteja na raiz), tenta o caminho direto
    if not os.path.exists(caminho):
        caminho = os.path.join(diretorio_atual, "data", "MICRODADOS_DIVERSIFICADO.csv")

    if not os.path.exists(caminho):
        st.error(f"Arquivo não encontrado! Verifique se 'data/MICRODADOS_DIVERSIFICADO.csv' existe no GitHub.")
        st.info(f"O Streamlit tentou procurar em: {caminho}")
        return pd.DataFrame()

    # 3. Leitura do arquivo
    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="iso-8859-1",
        low_memory=False
    )
    
    # OTIMIZAÇÃO CRÍTICA
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("category")

    return df
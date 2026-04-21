import pandas as pd
import streamlit as st

def faixa_etaria(df):
    col = "IdadeNaDataNotificacao"
    
    if col not in df.columns:
        return pd.DataFrame(columns=["FaixaEtaria", "Quantidade"])

    # --- EXTRAÇÃO DIRETA DOS ANOS ---
    # O regex r'^(\d+)' pega apenas os números no INÍCIO da frase
    # Ex: "17 anos, 3 meses" -> 17
    # Ex: "0 anos, 1 meses" -> 0
    df['Idade_Anos'] = df[col].astype(str).str.extract(r'^(\d+)').astype(float).fillna(0).astype(int)

    # Definindo os intervalos (bins)
    # 0 a 18, 19 a 30, etc.
    bins = [-1, 18, 30, 45, 60, 75, 120]
    labels = ["0-18", "19-30", "31-45", "46-60", "61-75", "76+"]

    # Criando a coluna de faixas
    df["FaixaEtaria_Grafico"] = pd.cut(df["Idade_Anos"], bins=bins, labels=labels)

    # Agrupando para o Streamlit exibir
    dados = df["FaixaEtaria_Grafico"].value_counts().sort_index().reset_index()
    dados.columns = ["FaixaEtaria", "Quantidade"]

    return dados
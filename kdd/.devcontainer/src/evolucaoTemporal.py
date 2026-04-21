import pandas as pd

def evolucao_temporal(df):
    col_data = "DataNotificacao"
    
    if col_data not in df.columns:
        col_data = next((c for c in df.columns if 'Data' in c), None)

    if not col_data:
        return pd.DataFrame(columns=["AnoMes", "Quantidade"])

    # 2. Converte para datetime
    # O errors="coerce" transforma datas malucas em NaT (Not a Time) para não travar
    df[col_data] = pd.to_datetime(df[col_data], errors="coerce")

    # 3. Cria a coluna Ano-Mês e transforma em STRING
    # O Streamlit/Plotly lida melhor com strings do que com objetos Period do Pandas
    df["AnoMes"] = df[col_data].dt.to_period("M").astype(str)

    # 4. Agrupa e conta
    dados = df[df["AnoMes"] != "NaT"].groupby("AnoMes").size().reset_index(name="Quantidade")

    # Ordena cronologicamente
    return dados.sort_values("AnoMes")
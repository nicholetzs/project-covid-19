def top_municipios(df):
    dados = df["Municipio"].value_counts().head(10).reset_index()
    dados.columns = ["Municipio", "Número de Notificações"]
    return dados
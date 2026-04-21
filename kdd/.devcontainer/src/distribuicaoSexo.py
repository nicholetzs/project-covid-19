def distribuicao_sexo(df):
    dados = df["Sexo"].value_counts().reset_index()
    dados.columns = ["Sexo", "Frequência"]
    return dados
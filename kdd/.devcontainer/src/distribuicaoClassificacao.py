def distribuicao_classificacao(df):
    dados = df["Classificacao"].value_counts().reset_index()
    dados.columns = ["Classificacao", "Frequência Absoluta"]
    return dados
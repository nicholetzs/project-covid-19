def taxa_letalidade(df):
    total = len(df)
    obitos = (df["Evolucao"] == "Óbito pelo COVID-19").sum()

    taxa = (obitos / total) * 100 if total > 0 else 0

    return {"taxa": taxa}
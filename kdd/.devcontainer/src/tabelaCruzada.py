import pandas as pd


def tabela_cruzada(df):
    top5 = df["Municipio"].value_counts().head(5).index

    filtrado = df[df["Municipio"].isin(top5)]

    crosstab = pd.crosstab(filtrado["Municipio"], filtrado["Evolucao"])

    letalidade = {}

    for municipio in crosstab.index:
        total = crosstab.loc[municipio].sum()
        obitos = crosstab.loc[municipio].get("Óbito pelo COVID-19", 0)

        letalidade[municipio] = (obitos / total) * 100 if total > 0 else 0

    return crosstab, letalidade
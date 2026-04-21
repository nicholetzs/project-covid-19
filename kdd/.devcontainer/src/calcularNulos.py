import pandas as pd

def calcular_nulos(df):
    nulos = df.isnull().sum()
    total = len(df)

    resultado = pd.DataFrame({
        "Coluna": nulos.index,
        "Quantidade": nulos.values,
        "Percentual (%)": (nulos.values / total) * 100
    })

    return resultado[resultado["Quantidade"] > 0]
import pandas as pd

def sintomas_frequentes(df):
    sintomas_map = {
        "Febre": "Febre",
        "Tosse": "Tosse",
        "Garganta": "DorGarganta",
        "Dificuldade Respiratória": "DificuldadeRespiratoria",
        "Coriza": "Coriza",
        "Diarreia": "Diarreia",
        "Cefaleia": "Cefaleia"
    }
    
    dados = {}
    for label, col_real in sintomas_map.items():
        if col_real in df.columns:
            # Comparamos com "Sim" ignorando espaços ou letras minúsculas
            dados[label] = (df[col_real].astype(str).str.strip().str.capitalize() == "Sim").sum()
        else:
            # Se a coluna não existir, não quebra o código, apenas coloca 0
            dados[label] = 0

    # Cria o DataFrame para o gráfico
    df_sintomas = pd.DataFrame(list(dados.items()), columns=["Sintoma", "Quantidade"])
    
    # Ordena do maior para o menor
    return df_sintomas.sort_values(by="Quantidade", ascending=False)
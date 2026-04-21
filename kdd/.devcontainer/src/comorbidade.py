import pandas as pd

def comorbidades_obitos(df):
    # 1. Identificar a coluna de Óbito (na sua amostra parece ser 'DataObito' ou 'Evolucao')
    # Vamos considerar que 'Evolucao' indica se foi óbito. 
    # Se a coluna Evolucao for 'Óbito', filtramos ela.
    col_evolucao = next((c for c in df.columns if c.lower() == 'evolucao'), None)
    
    if col_evolucao:
        # Filtra apenas quem tem algum registro de óbito (ajuste conforme seu dado real)
        df_obitos = df[df[col_evolucao].astype(str).str.contains("Óbito|SIM", case=False, na=False)]
    else:
        # Se não achar a coluna, usa o DF inteiro para não quebrar o gráfico (ou retorna vazio)
        df_obitos = df

    # 2. Mapeamento das Comorbidades com os nomes REAIS do seu CSV
    comorb_map = {
        "Diabetes": "ComorbidadeDiabetes",
        "Cardiopatia": "ComorbidadeCardio",
        "Obesidade": "ComorbidadeObesidade",
        "Pulmão": "ComorbidadePulmao",
        "Renal": "ComorbidadeRenal",
        "Tabagismo": "ComorbidadeTabagismo"
    }

    dados = {}
    for label, col_real in comorb_map.items():
        if col_real in df_obitos.columns:
            # Conta quem tem a comorbidade e é óbito
            dados[label] = (df_obitos[col_real].astype(str).str.strip().str.upper() == "SIM").sum()
        else:
            dados[label] = 0

    return (
        pd.DataFrame(list(dados.items()), columns=["Comorbidade", "Quantidade"])
        .sort_values(by="Quantidade", ascending=False)
    )
import pandas as pd

def carrega_csv(df):
    df = pd.read_csv("data/vendas.csv")
    return df
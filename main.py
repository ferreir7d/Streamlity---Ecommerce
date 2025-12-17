import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comercial", page_icon=":credit_card:")

st.markdown("""
# Dashboard de Vendas
            
## Acompanhamento de Indicadores de Vendas

Visão consolidada de faturamento, ticket médio e performance da equipe comercial.
"""
            )

# widget de upload de dados
file_upload = st.file_uploader(
    label="Faça upload dos dados aqui", type=['csv'])

# verifica se o arquivo foi feito upload
if file_upload:

    # leitura dos dados
    df = pd.read_csv(file_upload)

    df['data_movimento'] = pd.to_datetime(df["data_movimento"]).dt.date

    # exibição dos dados
    exp1 = st.expander("Dados Brutos")
    fmt_columns = {"valor_solicitado": st.column_config.NumberColumn(
        "valor_solicitado", format="R$ %f")}
    exp1.dataframe(df, hide_index=True, column_config=fmt_columns)

    # visão vendas.
    exp2 = st.expander("Visão Das Vendas Dos Vendedores")
    df_pivot = df.pivot_table(
        index="data_movimento",
        columns="nome_vendedor",
        values="valor_emitido",
        aggfunc="sum",
        fill_value=0
    )


    #abas para diferentes visualizações
    tab_data, tab_history, tab_share = exp2.tabs(
        ["Dados", "Histórico", "Distribuição"])

    #exibe o dataframe
    with tab_data:
        st.dataframe(df_pivot)

    #exibe o histórico

    with tab_history:
        st.line_chart(df_pivot)

    #exibe a distribuição
    with tab_share:
        #filtro de data
        date = st.selectbox("Filtro Data", options=df_pivot.index)

        # Em vez de olhar só o último dia, somamos o total do período (Ranking)
        total_por_vendedor = df_pivot.sum().sort_values(ascending=False)

        # Gráfico de barras mostrando quem vendeu mais no total
        st.bar_chart(total_por_vendedor)

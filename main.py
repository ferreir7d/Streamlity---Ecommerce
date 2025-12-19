import streamlit as st
import pandas as pd
import plotly.express as px

#configuração da página
st.set_page_config(page_title="Dashboard Comercial", layout="wide", page_icon="🏦")

def carregar_dados():
    try:
        df = pd.read_csv("vendas.csv")
        df['data_movimento'] = pd.to_datetime(df['data_movimento'])
        return df
    except FileNotFoundError:
        return None

df = carregar_dados()

# --- TÍTULO E CABEÇALHO ---
st.title("📊 Dashboard de Performance Comercial")
st.markdown("Visão consolidada de vendas, ranking de vendedores e mix de produtos.")
st.markdown("---")

if df is None:
    st.error("Erro: O arquivo 'vendas.csv' não foi encontrado na pasta.")
    st.stop()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros")
# Filtro de Regional
regionais = ["Todas"] + list(df['regional'].unique())
regional_selecionada = st.sidebar.selectbox("Selecione a Regional", regionais)

# Aplica o filtro no DataFrame
if regional_selecionada != "Todas":
    df_filtrado = df[df['regional'] == regional_selecionada]
else:
    df_filtrado = df

# --- KPIS (INDICADORES TOPO) ---
col1, col2, col3 = st.columns(3)

# Cálculo dos Totais
total_vendas = df_filtrado['valor_emitido'].sum()
ticket_medio = df_filtrado['valor_emitido'].mean()
total_contratos = df_filtrado.shape[0]

with col1:
    st.metric("Total Vendido", f"R$ {total_vendas:,.2f}")
with col2:
    st.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
with col3:
    st.metric("Contratos Emitidos", total_contratos)

st.markdown("---")

# --- GRÁFICOS (LINHA 1) ---
col_graf1, col_graf2 = st.columns([2, 1])

with col_graf1:
    st.subheader("Evolução Diária de Vendas")
    # Agrupa por dia para fazer a linha do tempo
    df_timeline = df_filtrado.groupby("data_movimento")["valor_emitido"].sum().reset_index()
    
    fig_linha = px.line(
        df_timeline, 
        x="data_movimento", 
        y="valor_emitido",
        markers=True,
        template="plotly_white"
    )
    fig_linha.update_layout(xaxis_title="", yaxis_title="Valor (R$)")
    st.plotly_chart(fig_linha, use_container_width=True)


# --- GRÁFICOS (LINHA 2) ---
st.subheader("🏆 Ranking de Vendedores")

# Prepara dados para o ranking
df_vendedores = df_filtrado.groupby("nome_vendedor")[["valor_emitido", "meta_vendedor"]].sum().reset_index()
df_vendedores = df_vendedores.sort_values(by="valor_emitido", ascending=False)

fig_barras = px.bar(
    df_vendedores,
    x="nome_vendedor",
    y="valor_emitido",
    text_auto='.2s', # Formatação automática de K/M
    color="valor_emitido", # Cor baseada no valor
    color_continuous_scale="Blues",
    template="plotly_white"
)
fig_barras.update_layout(xaxis_title="", yaxis_title="Total Vendido (R$)")
st.plotly_chart(fig_barras, use_container_width=True)

with st.expander("📂 Ver Base de Dados Detalhada"):
    st.dataframe(
        df_filtrado,
        column_config={
            "valor_solicitado": st.column_config.NumberColumn(format="R$ %.2f"),
            "valor_emitido": st.column_config.NumberColumn(format="R$ %.2f"),
            "data_movimento": st.column_config.DateColumn("Data")
        },
        hide_index=True
    )
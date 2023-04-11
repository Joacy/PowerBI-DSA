import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import os

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
from datetime import date, datetime, timedelta

st.set_page_config(
  page_title="Dashboard Analítico de Vendas Globais",
  page_icon="📈",
  layout="wide"
)

df_vendas = pd.read_csv("dataset.csv", sep=";")

datas = []
anos = []
for data in df_vendas["Data_Pedido"]:
  data_datetime = datetime.strptime(data, '%d-%m-%Y').date()
  anos.append(data_datetime.year)
  datas.append(data_datetime)
df_vendas["Data_Pedido"] = datas
df_vendas["Ano_Pedido"] = anos

descontos = []
for d in df_vendas["Desconto"]:
  descontos.append(float(d.replace(",", ".")))
df_vendas["Desconto"] = descontos

lucro = []
for l in df_vendas["Lucro"]:
  lucro.append(float(l.replace(",", ".")))
df_vendas["Lucro"] = lucro

total_vendas = []
for total in df_vendas["Total_Vendas"]:
  total_vendas.append(float(total.replace(",", ".")))
df_vendas["Total_Vendas"] = total_vendas

title, version = st.columns([10, 2], gap="large")

title.markdown("## Laboratório Prático 01 - Dashboard Analítico de Vendas Globais")
version.markdown("###### Versão 1.0")
version.markdown("###### joacymsilva@gmail.com")

st.text("")
col1, col2, col3 = st.columns([2, 5, 5], gap="large")
st.text("")
col4, col5 = st.columns([6, 6], gap="large")

ano_venda = st.sidebar.select_slider(label="Ano", options=sorted(set(anos)))
st.sidebar.text("")
segmento = st.sidebar.selectbox("Segmento", (sorted(df_vendas["Segmento"].unique())))
st.sidebar.text("")
# Add vertical scroll for radio.
st.markdown("""
    <style>
        .row-widget.stRadio {
          max-height: 300px;
          overflow-y: scroll;
        }
    </style>
    """,
    unsafe_allow_html=True)
pais = st.sidebar.radio("País", (sorted(df_vendas["Pais"].unique())))


col1.metric(label="Valor Total Vendido", value=f"{round(df_vendas['Total_Vendas'].sum()/1000000, 2)} Mi")

col2.markdown("Total de Vendas por Categoria")
df_total_vendas_por_categoria = df_vendas[['Total_Vendas', 'Categoria']].groupby(['Categoria']).sum().reset_index()
col2.bar_chart(df_total_vendas_por_categoria, x='Categoria', y="Total_Vendas")

col3.markdown("Média de Desconto por SubCategoria de Produto")
df_media_desconto_por_subcategoria = df_vendas[['Desconto', 'SubCategoria']].groupby(['SubCategoria']).mean().sort_values(by='Desconto', ascending=False).reset_index()
# fig2 = go.Figure()
# fig2.add_trace(go.Bar(x=df_media_desconto_por_categoria["Desconto"], y=df_media_desconto_por_categoria["SubCategoria"], orientation='h'))
# fig2.update_layout(xaxis_rangeslider_visible=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
# col3.plotly_chart(fig2, use_container_width=True)
col3.bar_chart(df_media_desconto_por_subcategoria, x='SubCategoria', y="Desconto")

col4.markdown("Média de Total de Vendas por Pais, acima de 250")

col5.markdown("Quantidade de Vendas por Pais e por Prioridade de Entrega")
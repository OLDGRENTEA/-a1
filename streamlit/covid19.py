import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

@st.cache(suppress_st_warning=True)
def load_data():
    data = pd.read_csv('COVID-19-global-data.csv')
    return data
covid_data = load_data()

st.sidebar.checkbox("世卫组织冠状病毒 (COVID-19) 仪表板", True, key=1)
df = covid_data.groupby(by=['Country']).sum().reset_index()
select = st.sidebar.selectbox('选择一个国家', df['Country'])

# 获取选择框选中的状态
state_data = df[df['Country'] == select]
select_status = st.sidebar.radio("世卫组织冠状病毒 (COVID-19)病例",
                                 ('新增病例', '累计病例', '新增死亡病例', '累计死亡病例'))


def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({
        '病例分类': ['新增病例', '累计病例', '新增死亡病例', '累计死亡病例'],
        '病例数': (dataset.iloc[0]['New_cases'],
                dataset.iloc[0]['Cumulative_cases'],
                dataset.iloc[0]['New_deaths'], dataset.iloc[0]['Cumulative_deaths'])})
    return total_dataframe


state_total = get_total_dataframe(state_data)

if st.sidebar.checkbox("世卫组织冠状病毒 (COVID-19) 仪表板", True, key=2):
    st.markdown("## **世卫组织冠状病毒 (COVID-19) 仪表板**")
    st.markdown("### %s 国家总新增病例、累计病例、新增死亡病例和累计死亡病例" % (select))
    if not st.checkbox('Hide Graph', False, key=1):
        state_total_graph = px.bar(
            state_total,
            x='病例分类',
            y='病例数',
            labels={'病例数': '%s 国家的总病例数' % (select)},
            color='病例分类')
        st.plotly_chart(state_total_graph)


def get_table():
    datatable = df.sort_values(by=['Cumulative_cases'], ascending=False)
    return datatable


datatable = get_table()
st.markdown("### 世界各国家的Covid-19病例分析")
st.markdown("下表为您提供了 %s 国家Covid-19总新增病例、累计病例、新增死亡病例和累计死亡病例的实时分析。" % (select))
st.dataframe(datatable)  # will display the dataframe
#安装
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import datetime

#加载数据集（数据来源：WHO）
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_data():
    data = pd.read_csv('COVID-19-global-data.csv', encoding='gb2312', error_bad_lines=False, sep='\t')
    return data

covid_data = load_data()

con = st.container()

# 背景图片的网址
img_url = 'https://img.zcool.cn/community/01aae555aafd616ac72581780fbcf7.jpg?x-oss-process=image/resize,h_600/format,jpg/format,webp/quality,q_100'

# 修改背景样式
st.markdown('''<style>.css-fg4pbf{background-image:url(''' + img_url + ''');
background-size:100% 100%;background-attachment:fixed;}</style>
''', unsafe_allow_html=True)

# 侧边栏样式
st.markdown('''<style>#root > div:nth-child(1) > div > div > div > div >
section.css-1lcbmhc.e1fqkh3o3 > div.css-1adrfps.e1fqkh3o2
{background:rgba(255,255,255,0.5)}</style>''', unsafe_allow_html=True)

# 底边样式
st.markdown('''<style>#root > div:nth-child(1) > div > div > div > div >
section.main.css-1v3fvcr.egzxvld3 > div > div > div
{background-size:100% 100% ;background:rgba(207,207,207,0.9);
color:red; border-radius:5px;} </style>''', unsafe_allow_html=True)


def callback():
    pass
myradio = st.sidebar.radio(label = "世卫组织冠状病毒 (COVID-19) 仪表板,请选择分类标准",
                   options = ("国家","地区"), # 选项
                   index = 0, # 初始化选项
                   format_func = lambda x : f"{x}", #这是格式化函数，注意我把原始选项ABC修改了。一般地，跟字典或dataframe结合也很好用。
                   key = "radio_demo",
                   help = "会展示世卫组织冠状病毒的仪表板，你可以选择按国家分类或者按地区分类", # 看到组件右上角的问号了没？上去悬停一下。
                   on_change = callback, args = None, kwargs = None)

#数据可视化
if myradio == "国家":
    df = covid_data.groupby(by=['Country']).sum().reset_index()
    select = st.sidebar.selectbox('选择一个国家', df['Country'])

    # df1 = covid_data.groupby(by=['WHO_region']).sum().reset_index()
    # select1 = st.sidebar.selectbox('选择一个地区', df1['WHO_region'])

    # 获取选择框选中的状态
    state_data = df[df['Country'] == select]
    select_status = st.sidebar.radio("世卫组织冠状病毒 (COVID-19)病例",
                                    ('新增病例', '累计病例', '新增死亡病例', '累计死亡病例'), help="选择您需要查看的类别")
    # state_data1 = df1[df1['WHO_region'] == select]
    # select_status1 = st.sidebar.radio("地区世卫组织冠状病毒 (COVID-19)病例",
    #                                  ('新增病例', '累计病例', '新增死亡病例', '累计死亡病例'))

    #绘制图形
    def get_total_dataframe(dataset):
        total_dataframe = pd.DataFrame({
    '病例分类': ['新增病例', '累计病例', '新增死亡病例', '累计死亡病例'],
    '病例数': (dataset.iloc[0]['New_cases'],
                   dataset.iloc[0]['Cumulative_cases'],
                   dataset.iloc[0]['New_deaths'], dataset.iloc[0]['Cumulative_deaths'])})
        return total_dataframe
    state_total = get_total_dataframe(state_data)

    # state_total1 = get_total_dataframe(state_data1)


    st.markdown("## **世卫组织冠状病毒 (COVID-19) 仪表板**")
    st.markdown("#### **按不同国家分类**")
    st.markdown("### %s 国家总新增病例、累计病例、新增死亡病例和累计死亡病例" % (select))
    if not st.checkbox('Hide Graph', False, key=3):
            state_total_graph = px.bar(
                state_total,
                x='病例分类',
                y='病例数',
               labels={'病例数': '%s 国家的总病例数' % (select)},
                color='病例分类')
            st.plotly_chart(state_total_graph)

    df1 = covid_data
    st.markdown("下表为您提供了 %s 国家Covid-19 %s 一定时间内的实时分析。" % (select, select_status))

    leixing = "新增病例"
    if select_status == "新增病例" :
        leixing = "New_cases"
    elif select_status == "累计病例" :
        leixing = "Cumulative_cases"
    elif select_status == "新增死亡病例":
        leixing = "New_deaths"
    elif select_status == "累计死亡病例":
        leixing = "Cumulative_deaths"

    start_time = st.date_input("起始时间", value=(datetime.date(2020,1,3)))
    end_time = st.date_input("结束时间", value=(datetime.date(2022,11,25)))

    df1['Date_reported'] = pd.to_datetime(df1['Date_reported'], format='%Y-%m-%d')
    df1.index = df1['Date_reported']

    mask = df1[(df1['Country'] == select)]

    mask["Date_reported"] = pd.DatetimeIndex(mask["Date_reported"]).date
    mask1 = mask[mask['Date_reported'] >= start_time]
    mask2 = mask1[mask1['Date_reported'] <= end_time]
    st.line_chart(mask2[leixing])

    #显示数据框或表格
    def get_table():
        datatable = df.sort_values(by=['Cumulative_cases'], ascending=False)
        return datatable
    datatable = get_table()
    st.markdown("### 世界各国家的Covid-19病例分析")
    st.markdown("下表为您提供了 %s 国家Covid-19总新增病例、累计病例、新增死亡病例和累计死亡病例的实时分析。"% (select))
    st.dataframe(datatable) # will display the dataframe
    st.table(state_total)# will display the table

elif myradio == "地区":
    df = covid_data.groupby(by=['WHO_region']).sum().reset_index()
    select = st.sidebar.selectbox('选择一个地区', df['WHO_region'])

    # df1 = covid_data.groupby(by=['WHO_region']).sum().reset_index()
    # select1 = st.sidebar.selectbox('选择一个地区', df1['WHO_region'])

    # 获取选择框选中的状态
    state_data = df[df['WHO_region'] == select]
    select_status = st.sidebar.radio("世卫组织冠状病毒 (COVID-19)病例",
                                    ('新增病例', '累计病例', '新增死亡病例', '累计死亡病例'))
    # state_data1 = df1[df1['WHO_region'] == select]
    # select_status1 = st.sidebar.radio("地区世卫组织冠状病毒 (COVID-19)病例",
    #                                  ('新增病例', '累计病例', '新增死亡病例', '累计死亡病例'))

    #绘制图形
    def get_total_dataframe(dataset):
        total_dataframe = pd.DataFrame({
    '病例分类': ['新增病例', '累计病例', '新增死亡病例', '累计死亡病例'],
    '病例数': (dataset.iloc[0]['New_cases'],
                   dataset.iloc[0]['Cumulative_cases'],
                   dataset.iloc[0]['New_deaths'], dataset.iloc[0]['Cumulative_deaths'])})
        return total_dataframe
    state_total = get_total_dataframe(state_data)

    # state_total1 = get_total_dataframe(state_data1)


    st.markdown("## **世卫组织冠状病毒 (COVID-19) 仪表板**")
    st.markdown("#### **按不同地区分类**")
    st.markdown("### %s 地区总新增病例、累计病例、新增死亡病例和累计死亡病例" % (select))
    if not st.checkbox('Hide Graph', False, key=3):
            state_total_graph = px.bar(
                state_total,
                x='病例分类',
                y='病例数',
               labels={'病例数': '%s 地区的总病例数' % (select)},
                color='病例分类')
            st.plotly_chart(state_total_graph)

    df1 = covid_data
    st.markdown("下表为您提供了 %s 地区Covid-19 %s 一定时间内的实时分析。" % (select, select_status))

    leixing = "新增病例"
    if select_status == "新增病例" :
        leixing = "New_cases"
    elif select_status == "累计病例" :
        leixing = "Cumulative_cases"
    elif select_status == "新增死亡病例":
        leixing = "New_deaths"
    elif select_status == "累计死亡病例":
        leixing = "Cumulative_deaths"

    start_time = st.date_input("起始时间", value=(datetime.date(2020, 1, 3)))
    end_time = st.date_input("结束时间", value=(datetime.date(2022, 11, 25)))

    df1['Date_reported'] = pd.to_datetime(df1['Date_reported'], format='%Y-%m-%d')
    df1.index = df1['Date_reported']

    mask = df1[(df1['WHO_region'] == select)]

    mask["Date_reported"] = pd.DatetimeIndex(mask["Date_reported"]).date
    mask1 = mask[mask['Date_reported'] >= start_time]
    mask2 = mask1[mask1['Date_reported'] <= end_time]
    st.line_chart(mask2[leixing])


    # df1 = df1[start_time:end_time]
    # st.dataframe(df1)

    #显示数据框或表格
    def get_table():
        datatable = df.sort_values(by=['Cumulative_cases'], ascending=False)
        return datatable
    datatable = get_table()
    st.markdown("### 世界各地区的Covid-19病例分析")
    st.markdown("下表为您提供了 %s 地区Covid-19总新增病例、累计病例、新增死亡病例和累计死亡病例的实时分析。"% (select))
    st.dataframe(datatable) # will display the dataframe
    st.table(state_total)# will display the table


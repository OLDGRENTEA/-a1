#安装
from __future__ import print_function
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import datetime
import requests
import json
import sys
import importlib
import json
from textrank4zh import TextRank4Sentence


#加载数据集（数据来源：WHO）
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_data():
    data = pd.read_csv('COVID-19-global-data.csv', encoding='gb2312', error_bad_lines=False, sep='\t')
    return data


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
myradio = st.sidebar.radio(label = "新闻文本摘要，请选择使用模型",
                   options = ("ChatGLM","TextRank4ZH"), # 选项
                   index = 0, # 初始化选项
                   format_func = lambda x : f"{x}", #这是格式化函数，注意我把原始选项ABC修改了。一般地，跟字典或dataframe结合也很好用。
                   key = "radio_demo",
                   help = "可以选择使用模型", # 看到组件右上角的问号了没？上去悬停一下。
                   on_change = callback, args = None, kwargs = None)

#数据可视化
if myradio == "ChatGLM":

    st.markdown("## **请在此处输入新闻内容**")

    #TODO

    prompt = st.text_input("在此处粘贴新闻文本", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None,
                  on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)

    st.markdown("下面是提取的摘要" )



    # https://u22566-bf38-de359af7.neimeng.seetacloud.com:6443/
    url = 'http://region-31.seetacloud.com:23991/'
    #prompt = '生成摘要' + '\n' + '11日下午，中共中央政治局常委、中央书记处书记刘云山登门看望了国家最高科技奖获得者于敏、张存浩。刘云山指出，广大科技工作者要学习老一辈科学家求真务实的钻研精神，淡泊名利、潜心科研，努力创造更多一流科研成果。'
    data = {'prompt': '生成摘要' + '\n' + prompt, 'history': []}
    response = requests.post(url, data=json.dumps(data))
    present_data = response.json()['response']

    st.markdown(present_data)

elif myradio == "TextRank4ZH":

    st.markdown("## **请在此处输入新闻内容**")

    #TODO

    prompt = st.text_input("在此处粘贴新闻文本", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None,
                  on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)

    st.markdown("下面是提取的摘要" )


    try:
        importlib.reload(sys)
        sys.setdefaultencoding('utf-8')
    except:
        pass

    import codecs

    generate = ""
    # tr4w.analyze(text=i, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    print()
    # print('摘要：')
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=prompt, lower=True, source='all_filters')
    for item in tr4s.get_key_sentences(num=2):
        generate += item.sentence
    # print(generate)
    hypothesis = generate


    present_data = hypothesis

    st.markdown(present_data)


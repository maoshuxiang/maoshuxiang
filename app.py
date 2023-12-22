import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import jieba
#Pyecharts是用于生成图表和可视化的Python库，WordCloud类用于创建词云图
from pyecharts.charts import WordCloud
from pyecharts import options as opts
#数据可视化库，用于创建柱状图（Bar）、饼图（Pie）、折线图（Line）和雷达图（Radar）、Scatter（散点图）
from pyecharts.charts import Bar, Pie, Line, Radar,Scatter,Tree
import matplotlib.pyplot as plt

#用正则表达式去除HTML标签 
def remove_html(text):  
    return re.sub('<[^<]+?>', '', text)  

#去除文本中的标点符号
def remove_sign(text):  
    text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
    return text

# 词频统计（过滤低频词，出现次数大于或等于阈值3的词才会被保留在词频统计结果中）
def count_word_freq(text, threshold=3):
    word_freq = Counter(jieba.cut(text))
    word_freq = {word: freq for word, freq in word_freq.items() if freq >= threshold}
    return word_freq

#词频统计,l过滤低频词
def count_word_freq(text):  
    word_freq = Counter(jieba.cut(text)) 

    return word_freq

#绘制词云图
def draw_cloud_chart(data):
    words_dict = {w[0]: w[1] for w in data}
    c = (
        WordCloud()
        #添加内容
        .add("", [list(w) for w in words_dict.items()],word_size_range=[20, 100])

        #设置图表标题
        .set_global_opts(title_opts=opts.TitleOpts(title="词云图"))
        #将词云图保存为html文件
        .render("wordcloud.html")
    )

    #在Streamlit中显示HTML内容
    st.components.v1.html(open('wordcloud.html', 'r', encoding='utf-8').read(), height=600,width=800)

#绘制柱状图
def draw_histogram_chart(data):
    x_axis = [x[0] for x in data]
    y_axis = [x[1] for x in data]
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis("", y_axis)
        .set_global_opts(title_opts=opts.TitleOpts(title="柱状图"))
        .render("histogram_chart.html")
    )
    st.components.v1.html(open('histogram_chart.html', 'r', encoding='utf-8').read(), height=600,width=850)

#绘制面积图
def draw_area_chart(data):
    line_chart = (
        Line()
        .add_xaxis([x[0] for x in data])
        .add_yaxis("面积图", [x[1] for x in data], is_smooth=True)
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5)  # 设置面积填充样式
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="面积图"),
            xaxis_opts=opts.AxisOpts(name="词汇"),
            yaxis_opts=opts.AxisOpts(name="词频")
        )
        .render("area_chart.html")
    )
    st.components.v1.html(open('area_chart.html', 'r', encoding='utf-8').read(), height=600,width=870)


#绘制饼状图
def draw_pie_chart(data):
    c = (
        Pie()
        .add("",data)
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("pie_chart.html")
    )
    st.components.v1.html(open('pie_chart.html', 'r', encoding='utf-8').read(), height=600,width=800)

#绘制折线图
def draw_line_chart(data):
    x_axis = [x[0] for x in data]
    y_axis = [x[1] for x in data]
    c = (
        Line()
        .add_xaxis(x_axis)
        .add_yaxis("", y_axis, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="折线图"))
        .render("line_chart.html")
    )
    st.components.v1.html(open('line_chart.html', 'r', encoding='utf-8').read(), height=600,width=850)

#绘制散点图
def draw_scatter_chart(data):
    x_axis = [x[0] for x in data]
    y_axis = [x[1] for x in data]
    c = (
        Scatter()
        .add_xaxis(x_axis)
        .add_yaxis("", y_axis)
        # 设置散点图的其他属性
        .set_global_opts(title_opts=opts.TitleOpts(title="散点图"))
        .render("scatter_chart.html")
    )
    st.components.v1.html(open('scatter_chart.html', 'r', encoding='utf-8').read(), height=800,width=850)

#绘制雷达图
def draw_radar_chart(data):
    x_axis = [x[0] for x in data]
    y_axis = [x[1] for x in data]
    radar = (
        Radar()
        .add_schema(
            schema=[
            #设置雷达图的指标项，假设最大值为30
                opts.RadarIndicatorItem(name=x, max_=30) for x in x_axis
            ]
        )
        .add(series_name="", data=[y_axis])
        .set_global_opts(title_opts=opts.TitleOpts(title="雷达图"))
        .render("radar_chart.html")
    )
    # 显示图表
    st.components.v1.html(open('radar_chart.html', 'r', encoding='utf-8').read(), height=850)

def main():
    # 设置 Streamlit 应用的标题image.png
    st.title('My Streamlit')

    # 创建一个文本输入框，用于接收用户输入的要爬取的网站地址
    url = st.text_input('请输入要爬取的网站地址：', max_chars=500)

    if url:
        # 发送 GET 请求获取指定网站的内容
        res = requests.get(url)
        
        #根据 HTTP 响应的内容类型解析编码方式
        encoding = res.encoding if 'charset' in res.headers.get('content-type', '').lower() else None

        # 使用 BeautifulSoup 将网站内容解析为 BeautifulSoup 对象
        soup = BeautifulSoup(res.content, 'html.parser', from_encoding=encoding)

        # 获取网站文本内容
        text = soup.get_text()

        #调用去除标签方法  
        text = remove_html(text)

        #调用去除符号方法  
        text = remove_sign(text) 

        #调用方法对获取的文本内容进行分词，统计词频
        word_freq=count_word_freq(text)

        # 在左侧栏添加图形筛选器
        chart_type = st.sidebar.selectbox("选择图形", options=['词云图', '柱状图', '面积图','饼状图', '折线图', '散点图','雷达图'])

        #收集词频排名前20的词汇
        data=[(word,freq) for word,freq in word_freq.most_common(20)]

        if chart_type=='词云图':
            #调用方法，绘制词云图
            draw_cloud_chart(data)
        elif chart_type=='柱状图':
            #调用方法，绘制词云图
            draw_histogram_chart(data)
        elif chart_type=='面积图':
            draw_area_chart(data)
        elif chart_type=='饼状图':
            draw_pie_chart(data)
        elif chart_type=='折线图':
            draw_line_chart(data)
        elif chart_type=='散点图':
            draw_scatter_chart(data)
        elif chart_type=='雷达图':
            draw_radar_chart(data)
            
if __name__ == '__main__':  
    main()
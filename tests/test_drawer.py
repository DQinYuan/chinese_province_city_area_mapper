import cpca
from cpca import drawer
import pandas as pd
import os

origin_addr = pd.read_csv(os.path.join(os.path.dirname(__file__), 'addr.csv'))
df = cpca.transform(origin_addr['原始地址'])


def test_draw_locations():
    """使用folium绘制热力图"""
    drawer.draw_locations(df, "df.html")


def test_echarts_draw():
    """使用echarts绘制热力图"""
    drawer.echarts_draw(df,
                        "df_echarts.html", title="地域分布图", subtitle="location distribute")


def test_echarts_cate_draw():
    """使用echarts绘制分类散点图"""
    drawer.echarts_cate_draw(df, df['省'], "df_echarts_cate.html")

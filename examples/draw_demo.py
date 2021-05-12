# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import sys

import pandas as pd

sys.path.append('..')
import addressparser
from addressparser import drawer

if __name__ == '__main__':
    origin = pd.read_csv("../tests/addr.csv")
    # 转换
    addr_df = addressparser.transform(origin["原始地址"])
    # 输出
    processed = pd.concat([origin, addr_df], axis=1)
    processed.to_csv("processed.csv", index=False, encoding="utf-8")

    drawer.echarts_draw(addr_df, "df_echarts.html", title="地域分布图", subtitle="location distribute")

    drawer.echarts_cate_draw(addr_df, addr_df['省'], "df_echarts_cate.html")

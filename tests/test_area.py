# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import addressparser

def test_error_area():
    """3级地名出错bug"""

    print(addressparser.__version__)
    location_str = [
        "北京市昌平区昌平路97号新元科技园B座504",
        "上海经静安区大田路靠近北京西路",
        "成都市高新区天府大道399号天府新谷",
        "青岛市市南区浙江路14号2楼",
        "重庆市渝北区新牌坊一路136号",
        "北京市朝阳区裕民路12号中国国际科技会展中心A座1005",
        "南京市江宁区润发路18号",
        "杭州市西湖区文一西路75号",
        "杭州市下城区朝晖路168号钛合国际A座1204室",
    ]
    print('-' * 42)
    df = addressparser.transform(location_str, cut=True)
    print(df)

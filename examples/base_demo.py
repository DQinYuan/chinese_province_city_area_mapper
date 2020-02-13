# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

location_str = ["徐汇区虹漕路461号58号楼5楼",
                "泉州市洛江区万安塘西工业区",
                "朝阳区北苑华贸城",
                "收货人:xxx, 地址:湖北恩施州建始县业州镇湖北省建始县桂苑小区二单元111-2, 电话:13593643115",
                "收货人:木鱼, 地址:浙江嘉兴市海宁市许村镇浙江省海宁市许村镇茗山村徐家石桥1号, 电话:13593643115",
                ]
import cpca

df = cpca.transform(location_str)
print(df)

print("-" * 42)
df2 = cpca.transform(location_str, cut=False)
print(df2)

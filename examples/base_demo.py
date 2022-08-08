# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import sys

sys.path.append('..')
import addressparser

if __name__ == '__main__':
    location_str = ["徐汇区虹漕路461号58号楼5楼",
                    "泉州市洛江区万安塘西工业区",
                    "朝阳区北苑华贸城",
                    "上海浦东新区城区昌邑路1669弄7号602（苗圃路口）",
                    "湖北天门市渔薪镇湖北省天门市三渔薪镇王湾村六组",
                    "收货人:xxx, 地址:湖北恩施州建始县业州镇湖北省建始县桂苑小区二单元111-2, 电话:1359",
                    "收货人:木鱼, 地址:浙江嘉兴市海宁市许村镇浙江省海宁市许村镇茗山村徐家石桥1号, 电话:135936",
                    "山东钢城区桂苑小区二单元11号是新增地区",
                    "台湾屏东县三地门紫竹小区11号",
                    "香港新界北区银座大厦A座1号楼1层",
                    ]
    df = addressparser.transform(location_str)
    print(df)

    for map_key in zip(df["省"], df["市"], df["区"]):
        print(map_key)

    for map_key in zip(df["省"], df["市"], df["区"]):
        print(' '.join([i for i in map_key]))

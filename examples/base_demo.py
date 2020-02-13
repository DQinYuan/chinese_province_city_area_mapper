# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import address_extractor

if __name__ == '__main__':
    location_str = ["徐汇区虹漕路461号58号楼5楼",
                    "泉州市洛江区万安塘西工业区",
                    "朝阳区北苑华贸城",
                    "湖北天门市渔薪镇湖北省天门市三渔薪镇王湾村六组",
                    "收货人:xxx, 地址:湖北恩施州建始县业州镇湖北省建始县桂苑小区二单元111-2, 电话:13593643115",
                    "收货人:木鱼, 地址:浙江嘉兴市海宁市许村镇浙江省海宁市许村镇茗山村徐家石桥1号, 电话:13593643115",
                    ]
    locations = address_extractor.transform(location_str)
    print(locations)

    for map_key in zip(locations["省"], locations["市"], locations["区"]):
        print(map_key)

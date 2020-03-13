# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import addressparser


def test_error_province():
    """一级地名出错bug修复"""
    location_str = [
        "宁波市江东区兴宁路42弄1号金汇大厦12楼",
        "天津空港经济区环河北路80号空港商务园东区",
        "龙华新区创业路汇海广场C座20楼",  # 无匹配
        "龙华创业路汇海广场C座20楼",
        "田林路140号越界创意园16号楼东402室",
        "上海浦东商城路1287号1幢5楼",
        "成都市高新区高朋大道12号府河电器孵化基地B座307 （永丰立交桥西）",
        "上海市浦东新区张杨路400号源一创意办公中心D101室",
        "田林路388号1号楼新业大楼1楼西侧102室",
        "上海市浦东新区东方路1365号5号楼24B",
        "珠江新城广晟国际大厦801室",
    ]
    print('-' * 42)
    df = addressparser.transform(location_str)
    print(df)


def test_place():
    """级联地名出错bug"""
    location_str = [
        "天津空港经济区环河北路80号空港商务园东区",
    ]
    df = addressparser.transform(location_str)
    print(df)

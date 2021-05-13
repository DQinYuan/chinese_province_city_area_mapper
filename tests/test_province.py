# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import sys

sys.path.append('..')
import addressparser


def test_error_province():
    """一级地名出错bug修复"""
    location_str = [
        "宁波市江东区兴宁路42弄1号金汇大厦12楼",
        "天津空港经济区环河北路80号空港商务园东区",
        "龙华新区创业路汇海广场C座20楼",  # 无匹配
        "龙华创业路汇海广场C座20楼",
        "田林路140号越界创意园16号楼东402室",
        "上海市浦东新区东方路1365号5号楼24B",
        "上海浦东商城路1287号1幢5楼",
        "成都市高新区高朋大道12号府河电器孵化基地B座307 （永丰立交桥西）",
        "田林路388号1号楼新业大楼1楼西侧102室",
        "珠江新城广晟国际大厦801室",
    ]
    print('-' * 42)
    df = addressparser.transform(location_str)
    print(df)
    assert df.loc[0, '省'] == '浙江省'
    assert df.loc[1, '省'] == '天津市'
    assert df.loc[2, '省'] == ''
    assert df.loc[3, '省'] == ''
    assert df.loc[4, '省'] == ''
    assert df.loc[5, '省'] == '上海市'
    assert df.loc[6, '省'] == '上海市'
    assert df.loc[7, '省'] == '四川省'
    assert df.loc[8, '省'] == ''
    assert df.loc[9, '省'] == ''


def test_place():
    """级联地名出错bug"""
    location_str = [
        "天津空港经济区环河北路80号空港商务园东区",
    ]
    df = addressparser.transform(location_str)
    print(df)

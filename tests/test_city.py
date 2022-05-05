# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import sys

sys.path.append('..')
import addressparser


def string_dataframe(df):
    res = []
    for i in zip(df["省"], df["市"], df["区"]):
        res.append(i[0] + i[1] + i[2])
    return ' '.join(res)


def test_simple_area():
    """测试三级区划简称和二级区划简称的匹配"""
    location_str = ["上海市浦东新区虹漕路461号58号楼1楼",
                    "上海市浦东区虹漕路461号58号楼2楼",
                    "上海市浦东虹漕路461号58号楼3楼",
                    "天津滨海祥和小区",
                    "天津滨海区祥和小区",  # error with "区祥和小区"
                    "天津滨海新区小何小区111号",
                    "北京丰台区小何小区111号",
                    "孝感安陆小何小区111号",
                    "广西南宁市江南区城区南国花园5号",
                    "湖南益阳市安化县县城内湖南省益阳市安化县大福镇新桥",
                    "广西南宁市江南区城区南国花园5栋",
                    "湖北武汉武昌区复兴路1号",
                    "山西晋城市城区开发区怡凤小区凤巢小学对面10号楼"
                    ]
    df = addressparser.transform(location_str)
    print(df)


def test_city_detail():
    df_str = string_dataframe(addressparser.transform(['上海市浦东虹漕路461号58号楼5楼']))
    print(df_str)
    assert df_str == '上海市上海市浦东新区'


def test_city_detail_1():
    df_str = string_dataframe(addressparser.transform(['天津滨海新区小何小区111号']))
    print(df_str)
    assert df_str == '天津市天津市滨海新区'


def test_city_detail_2():
    df_str = string_dataframe(addressparser.transform(['孝感安陆小何小区111号']))
    print(df_str)
    assert df_str == '湖北省孝感市安陆市'


def test_city_detail_3():
    df_str = string_dataframe(addressparser.transform(['山西晋城市城区开发区怡凤小区凤巢小学对面10号楼']))
    print(df_str)


def test_predict_city():
    """预测市级地区"""
    location_str = ["河北北戴河融合小区11号",
                    "河北北戴河区融合小区11号",
                    ]
    print('-' * 42)
    df = addressparser.transform(location_str)
    print(df)

    df_str = string_dataframe(addressparser.transform(['河北北戴河区融合小区11号']))
    print(df_str)
    assert df_str == '河北省秦皇岛市北戴河区'


def test_predict_province():
    """预测省级地区"""
    location_str = ["秦皇岛北戴河融合小区11号",
                    "秦皇岛北戴河区融合小区11号",
                    ]
    print('-' * 42)
    df = addressparser.transform(location_str)
    print(df)

    df_str = string_dataframe(addressparser.transform(['秦皇岛北戴河区融合小区11号']))
    print(df_str)
    assert df_str == '河北省秦皇岛市北戴河区'


def test_error_city_jilin():
    """二级地名出错bug修复"""
    location_str = [
        "吉林通化市辉南县一中",
        "吉林通化市辉南县11号",
        "吉林省通化市辉南县11号",
        "吉林白山市临江市城区吉林省临江市新市街道鸭绿江花园1号",
        "吉林白山市临江市城区新市街道鸭绿江花园1号",
    ]
    df = addressparser.transform(location_str)
    print(df)


def test_error_city_hainan():
    """二级地名出错bug修复"""
    location_str = [
        "河北石家庄市桥西区校区公路11号",
        "海南白沙县金波乡金波乡金眉路2号",
        "海南乐东县九所镇乐东龙栖湾村东侧波波利海岸",
        "海南乐东黎族自治县九所镇乐东龙栖湾村东侧波波利海岸",
        "海南乐东县佛罗镇龙沐湾太阳商城C区7号楼",
        "海南保亭县保城镇七仙岭温泉国家森林公园温泉路8号龙湾雨林谷",
        "海南保亭县响水镇海南省保亭黎族苗族自治县响水镇2224国道西50米",
        "河南宽城县祥和小区22号",

    ]
    df = addressparser.transform(location_str)
    print(df)

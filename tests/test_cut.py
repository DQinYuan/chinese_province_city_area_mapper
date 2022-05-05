# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import os

import jieba

pwd_path = os.path.abspath(os.path.dirname(__file__))


def test_cut():
    """切词"""
    location_str = [
        "上海市浦东新区东方路1365号5号楼24B",
    ]
    for i in location_str:
        o = jieba.lcut(i)
        print(o)


def test_cut_with_dict():
    """加入自定义词典，切词"""
    d = {'上海': 1000, '浦东新区': 1000}
    d_path = 'my.dict'
    with open(d_path, 'w', encoding='utf-8') as f:
        for k, v in d.items():
            f.write(k + ' ' + str(v) + '\n')

    jieba.set_dictionary(d_path)
    location_str = [
        "上海市浦东新区东方路1365号5号楼24B",
        "上海浦东东方路1365号5号楼24B",
        "上海市浦东东方路1365号5号楼24B",
        "上海市浦东区东方路1365号5号楼24B",
    ]
    for i in location_str:
        o = jieba.lcut(i)
        print(i, o)
    os.remove(d_path)


def test_cut_custom_dict():
    """新增自定义词典，切词"""
    d_path = os.path.join(pwd_path, 'custom_word_freq.dict')

    location_str = [
        "上海市浦东新区东方路1365号5号楼24B",
        "上海浦东东方路1365号5号楼24B",
        "上海市浦东东方路1365号5号楼24B",
        "上海市浦东区东方路1365号5号楼24B",
        "湖北武汉复兴路111号",
        "天津滨海祥和小区",
        "天津滨海新区小何小区111号",
        "山西晋城市城区开发区怡凤小区凤巢小学对面10号楼",
        "孝感市安陆小何小区111号",
        "秦皇岛市北戴河融合小区11号",
        "吉林通化市辉南县一中",
        "北京市昌平区昌平路97号新元科技园B座504",
        "杭州市下城区朝晖路168号钛合国际A座1204室"
    ]
    for i in location_str:
        o = jieba.lcut(i)
        print(i, o)
    print('-' * 42)
    jieba.set_dictionary(d_path)
    for i in location_str:
        o = jieba.lcut(i)
        print(i, o)
    assert jieba.lcut("上海市浦东新区东方路1365号5号楼24B") == ['上海市', '浦东新区', '东方路', '1365', '号', '5', '号楼', '24B']
    assert jieba.lcut("湖北武汉复兴路111号") == ['湖北', '武汉', '复兴路', '111', '号']
    assert jieba.lcut("秦皇岛市北戴河融合小区11号") == ['秦皇岛市', '北戴河', '融合小区', '11', '号']

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
    d_path = os.path.join(pwd_path, '../addressparser/word_freq.dict')

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

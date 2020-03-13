# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import addressparser


def test_recheck():
    """级联地名出错bug"""
    location_str = [
        "天津空港经济区环河北路80号空港商务园东区",
    ]
    df = addressparser.transform(location_str)
    print(df)

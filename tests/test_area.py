# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import sys

sys.path.append('..')
import addressparser


def test_error_area():
    """3级地名测试"""
    print(addressparser.__version__)
    print('-' * 42)
    location_str = [
        "北京市昌平区昌平路97号新元科技园B座504",
        "上海经静安区大田路靠近北京西路",
        "青岛市市南区浙江路14号2楼",
        "北京市朝阳区裕民路12号中国国际科技会展中心A座1005",
        "杭州市下城区朝晖路168号钛合国际A座1204室",
    ]

    addr_df = addressparser.transform(location_str, pos_sensitive=True)
    print(addr_df)

    def _assert_line(linenum, province, city, area, addr,
                     province_pos=-1, city_pos=-1, area_pos=-1):
        assert addr_df.loc[linenum, '省'] == province
        assert addr_df.loc[linenum, '市'] == city
        assert addr_df.loc[linenum, '区'] == area
        assert addr_df.loc[linenum, '地名'] == addr
        assert addr_df.loc[linenum, '省_pos'] == province_pos
        assert addr_df.loc[linenum, '市_pos'] == city_pos
        assert addr_df.loc[linenum, '区_pos'] == area_pos

    _assert_line(0, '北京市', '北京市', '昌平区', '昌平路97号新元科技园B座504', 0, 0, 3)
    _assert_line(1, '上海市', '上海市', '静安区', '经静安区大田路靠近北京西路', 0, 0, 3)
    _assert_line(2, '山东省', '青岛市', '市南区', '浙江路14号2楼', -1, 0, 3)
    _assert_line(3, '北京市', '北京市', '朝阳区', '裕民路12号中国国际科技会展中心A座1005', 0, 0, 3)
    _assert_line(4, '浙江省', '杭州市', '下城区', '朝晖路168号钛合国际A座1204室', -1, 0, 3)

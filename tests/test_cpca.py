# -*- coding: utf-8 -*-

import pandas as pd
from mock import MagicMock

import cpca


def test_init_data():
    ad_2_addr_dict, matcher = cpca._init_data()
    assert matcher._get("上海")[0] == '上海'
    assert matcher._get("上海")[1][0] is ad_2_addr_dict["310000000000"]


def assert_addr(addr_df: pd.DataFrame, pos_sensitive=False):
    def _assert_line(linenum, province, city, area, addr, adcode,
                     province_pos=-1, city_pos=-1, area_pos=-1):
        assert addr_df.loc[linenum, cpca._PROVINCE] == province
        assert addr_df.loc[linenum, cpca._CITY] == city
        assert addr_df.loc[linenum, cpca._COUNTY] == area
        assert addr_df.loc[linenum, cpca._ADDR] == addr
        assert addr_df.loc[linenum, cpca._ADCODE] == adcode
        if pos_sensitive:
            assert addr_df.loc[linenum, cpca._PROVINCE_POS] == province_pos
            assert addr_df.loc[linenum, cpca._CITY_POS] == city_pos
            assert addr_df.loc[linenum, cpca._COUNTY_POS] == area_pos

    _assert_line(0, '上海市', '市辖区', '徐汇区', '虹漕路461号58号楼5楼', "310104", -1, -1, 0)
    _assert_line(1, '福建省', '泉州市', '洛江区', '万安塘西工业区', "350504", -1, 0, 3)
    _assert_line(2, '福建省', '福州市', '鼓楼区', '鼓楼医院', "350102", 0, -1, 3)
    _assert_line(3, '天津市', None, None, '', '120000', 0, -1, -1)
    _assert_line(4, "江苏省", "淮安市", "清江浦区", "人民路111号",
                 "320812", 6, 8, 10)
    _assert_line(5, "江苏省", "淮安市", "清江浦区", "上海路111号", "320812", 6, 8, 10)
    _assert_line(6, "上海市", "市辖区", "浦东新区", "东明路街道三林路15号", "310115", 0, -1, 3)
    _assert_line(7, "贵州省", "黔南布依族苗族自治州", "长顺县", "长寨街道和平中路28号", "522729", 0, 3, 13)
    _assert_line(8, "宁夏回族自治区", None, None, "", "640000", 0, -1, -1)


def test_transform():
    addr_list = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "福建省鼓楼区鼓楼医院",
                 "天津市",
                 "我家的地址是江苏淮安清江浦区人民路111号",
                 '我家的地址是江苏淮安清江浦区上海路111号',
                 "上海市浦东新区东明路街道三林路15号",
                 "贵州省黔南布依族苗族自治州长顺县长寨街道和平中路28号",
                 "宁夏"]
    transed = cpca.transform(addr_list)
    assert_addr(transed)

    # 测试pos_sensitive
    transed = cpca.transform(addr_list, pos_sensitive=True)
    assert_addr(transed, pos_sensitive=True)


def mock_map(monkeypatch, attrname, return_value, is_contain = True, is_unique_value = True):
    mock_map = MagicMock()
    mock_map.__contains__.return_value = is_contain
    mock_map.get_value.return_value = return_value
    mock_map.is_unique_value.return_value = is_unique_value
    monkeypatch.setattr(cpca, attrname, mock_map)
    return mock_map


def _dict2addr_map(mydict, valuedict = {}, is_unique_value = True):
    mock_map = MagicMock()

    mock_map.get_full_name.side_effect  = lambda key: mydict[key]
    mock_map.get_value.side_effect = lambda key, pca: valuedict[key]

    mock_map.__contains__.side_effect = lambda key: key in mydict
    mock_map.is_unique_value.return_value = is_unique_value
    return mock_map

# -*- coding: utf-8 -*-

import pandas as pd
from mock import MagicMock

import cpca


def test_init_data():
    ad_2_addr_dict, matcher = cpca._init_data()
    assert matcher._get("上海")[0] == '上海'
    assert matcher._get("上海")[1][0] is ad_2_addr_dict["310000000000"]


def assert_addr(addr_df: pd.DataFrame, pos_sensitive=False):
    _assert_line(addr_df, pos_sensitive, 0, '上海市', '市辖区', '徐汇区', '虹漕路461号58号楼5楼', "310104", -1, -1, 0)
    _assert_line(addr_df, pos_sensitive, 1, '福建省', '泉州市', '洛江区', '万安塘西工业区', "350504", -1, 0, 3)
    _assert_line(addr_df, pos_sensitive, 2, '福建省', '福州市', '鼓楼区', '鼓楼医院', "350102", 0, -1, 3)
    _assert_line(addr_df, pos_sensitive, 3, '天津市', None, None, '', '120000', 0, -1, -1)
    _assert_line(addr_df, pos_sensitive, 4, "江苏省", "淮安市", "清江浦区", "人民路111号",
                 "320812", 6, 8, 10)
    _assert_line(addr_df, pos_sensitive, 5, "江苏省", "淮安市", "清江浦区", "上海路111号", "320812", 6, 8, 10)
    _assert_line(addr_df, pos_sensitive, 6, "上海市", "市辖区", "浦东新区", "东明路街道三林路15号", "310115", 0, -1, 3)
    _assert_line(addr_df, pos_sensitive, 7, "贵州省", "黔南布依族苗族自治州", "长顺县", "长寨街道和平中路28号", "522729", 0, 3, 13)
    _assert_line(addr_df, pos_sensitive, 8, "宁夏回族自治区", None, None, "", "640000", 0, -1, -1)
    _assert_line(addr_df, pos_sensitive, 9, "江苏省", "淮安市", "市辖区", "", "320801", -1, 0, 3)
    _assert_line(addr_df, pos_sensitive, 10, None, None, None, None, None, -1, -1, -1)


def test_transform():
    addr_list = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "福建省鼓楼区鼓楼医院",
                 "天津市",
                 "我家的地址是江苏淮安清江浦区人民路111号",
                 '我家的地址是江苏淮安清江浦区上海路111号',
                 "上海市浦东新区东明路街道三林路15号",
                 "贵州省黔南布依族苗族自治州长顺县长寨街道和平中路28号",
                 "宁夏",
                 "淮安市市辖区",
                 # 测试错误数据
                 32323]
    transed = cpca.transform(addr_list)
    assert_addr(transed)

    # 测试pos_sensitive
    transed = cpca.transform(addr_list, pos_sensitive=True)
    assert_addr(transed, pos_sensitive=True)


def test_umap():
    addrs = ["朝阳区汉庭酒店大山子店", "吉林省朝阳区不知道店"]
    transed = cpca.transform(addrs, umap={"朝阳区": "110105"})
    _assert_line(transed, False, 0, "北京市", "市辖区", "朝阳区", "汉庭酒店大山子店", "110105", -1, -1, 0)
    _assert_line(transed, False, 1, "吉林省", "长春市", "朝阳区", "不知道店", "220104", 0, -1, 3)


def test_transform_text_with_addrs():
    addrs_text = "你家在吉林省朝阳区，而我家在北京市朝阳区，太远了"
    addr_df = cpca.transform_text_with_addrs(addrs_text, pos_sensitive=True)
    _assert_line(addr_df, True, 0, "吉林省", "长春市", "朝阳区", "", "220104", 3, -1, 6)
    _assert_line(addr_df, True, 1, "北京市", "市辖区", "朝阳区", "", "110105", 14, -1, 17)

    addrs_text = "吉林省北京市鼓楼区"
    addr_df = cpca.transform_text_with_addrs(addrs_text, pos_sensitive=True, umap={"鼓楼区": "320106"})
    _assert_line(addr_df, True, 0, "吉林省", None, None, "", "220000", 0, -1, -1)
    _assert_line(addr_df, True, 1, "北京市", None, None, "", "110000", 3, -1, -1)
    _assert_line(addr_df, True, 2, "江苏省", "南京市", "鼓楼区", "", "320106", -1, -1, 6)

    addrs_text = "天津市"
    addr_df = cpca.transform_text_with_addrs(addrs_text, pos_sensitive=True)
    _assert_line(addr_df, True, 0, "天津市", None, None, "", "120000", 0, -1, -1)
    assert len(addr_df) == 1

    addrs_text = "分店位于徐汇区虹漕路461号58号楼5楼和泉州市洛江区万安塘西工业区以及南京鼓楼区"
    addr_df = cpca.transform_text_with_addrs(addrs_text, pos_sensitive=True)
    assert len(addr_df) == 3
    _assert_line(addr_df, True, 0, "上海市", "市辖区", "徐汇区", "", "310104", -1, -1, 4)
    _assert_line(addr_df, True, 1, "福建省", "泉州市", "洛江区", "", "350504", -1, 21, 24)


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


def _assert_line(addr_df, pos_sensitive, linenum, province, city, area, addr, adcode,
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

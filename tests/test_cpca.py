# -*- coding: utf-8 -*-

import cpca
from cpca.structures import Pca
import pandas as pd
from mock import MagicMock
from cpca.structures import P,C,A


def assert_addr(addr_df: pd.DataFrame, pos_sensitive=False):
    def _assert_line(linenum, province, city, area, addr,
                     province_pos=-1, city_pos=-1, area_pos=-1):
        assert addr_df.loc[linenum, '省'] == province
        assert addr_df.loc[linenum, '市'] == city
        assert addr_df.loc[linenum, '区'] == area
        assert addr_df.loc[linenum, '地址'] == addr
        if pos_sensitive:
            assert addr_df.loc[linenum, '省_pos'] == province_pos
            assert addr_df.loc[linenum, '市_pos'] == city_pos
            assert addr_df.loc[linenum, '区_pos'] == area_pos

    _assert_line(0, '上海市', '上海市', '徐汇区', '虹漕路461号58号楼5楼', -1, -1, 0)
    _assert_line(1, '福建省', '泉州市', '洛江区', '万安塘西工业区', -1, 0, 3)
    _assert_line(2, '福建省', '福州市', '鼓楼区', '鼓楼医院', 0, -1, 3)


def test_transform():
    addr_list = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "福建省鼓楼区鼓楼医院"]
    # 分词模式
    transed = cpca.transform(addr_list)
    assert_addr(transed)

    # 全文匹配
    transed = cpca.transform(addr_list, cut=False)
    assert_addr(transed)

    # 测试pos_sensitive
    transed = cpca.transform(addr_list, pos_sensitive=True)
    print(transed)
    assert_addr(transed, pos_sensitive=True)


def test_data_from_csv():
    area_map, city_map, province_area_map, province_map, latlng = cpca._data_from_csv()
    print("....")
    assert province_map['北京'] == '北京市'
    assert city_map.get_full_name('北京') == '北京市'

    beijin_pca = [('北京市', '北京市', ''), ('北京市', '北京市', '东城区'), ('北京市', '北京市', '西城区'), ('北京市', '北京市', '朝阳区'), ('北京市', '北京市', '丰台区'), ('北京市', '北京市', '石景山区'), ('北京市', '北京市', '海淀区'), ('北京市', '北京市', '门头沟区'), ('北京市', '北京市', '房山区'), ('北京市', '北京市', '通州区'), ('北京市', '北京市', '顺义区'), ('北京市', '北京市', '昌平区'), ('北京市', '北京市', '大兴区'), ('北京市', '北京市', '怀柔区'), ('北京市', '北京市', '平谷区'), ('北京市', '北京市', '密云区'), ('北京市', '北京市', '延庆区')]
    assert city_map.get_relational_addrs('北京') == beijin_pca
    assert latlng[('北京市', '北京市', '东城区')] == ('39.93857401298612', '116.42188470126446')
    assert province_area_map.get_relational_addrs(('北京市', '东城区')) == [('北京市', '北京市', '东城区')]
    assert area_map.get_full_name('东城区') == '东城区'
    assert area_map.get_relational_addrs('东城区') == [('北京市', '北京市', '东城区')]


def mock_map(monkeypatch, attrname, return_value, is_contain = True, is_unique_value = True):
    mock_map = MagicMock()
    mock_map.__contains__.return_value = is_contain
    mock_map.get_value.return_value = return_value
    mock_map.is_unique_value.return_value = is_unique_value
    monkeypatch.setattr(cpca, attrname, mock_map)
    return mock_map


def test_fill_province(monkeypatch):
    pca = Pca('', '淮安市', '')
    
    # 猴子补丁
    mo_map = mock_map(monkeypatch, 'city_map', '江苏省')

    cpca._fill_province(pca)
    mo_map.get_value.assert_called_once_with(pca.city, P)
    assert pca.province == "江苏省"
    assert pca.city == '淮安市'


def test_fill_city_1():
    pca = Pca('', '', '朝阳区')
    cpca._fill_city(pca, {'朝阳区': '北京市'})
    assert pca.city == '北京市'


def test_fill_city_2(monkeypatch):
    pca = Pca('', '', '朝阳区')
    mo_map = mock_map(monkeypatch, 'area_map', '北京市')
    cpca._fill_city(pca, {})

    mo_map.get_value.assert_called_once_with(pca.area, C)
    assert pca.city == '北京市'


def test_fill_city_3(monkeypatch):
    pca = Pca('江苏省', '', '鼓楼区')
    mock_map(monkeypatch, 'area_map', '', is_contain=True, is_unique_value=False)
    mo_map = mock_map(monkeypatch, 'province_area_map', '南京市')
    cpca._fill_city(pca, {})

    mo_map.get_value.assert_called_once_with(('江苏省','鼓楼区'), C)
    assert pca.city == '南京市'


def _dict2addr_map(mydict, valuedict = {}, is_unique_value = True):
    mock_map = MagicMock()

    mock_map.get_full_name.side_effect  = lambda key: mydict[key]
    mock_map.get_value.side_effect = lambda key, pca: valuedict[key]

    mock_map.__contains__.side_effect = lambda key: key in mydict
    mock_map.is_unique_value.return_value = is_unique_value
    return mock_map


def test_jieba_extract(monkeypatch):
    """地址全部在句子开头的情况"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}))

    pca, addr = cpca._jieba_extract('江苏淮安清浦区人民路111号')

    assert addr == '人民路111号'
    assert pca.province == '江苏省'
    assert pca.province_pos == 0
    assert pca.city == '淮安市'
    assert pca.city_pos == 2
    assert pca.area == '清浦区'
    assert pca.area_pos == 4


def test_jieba_extract2(monkeypatch):
    """地址在句子中间的情况"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}))

    pca, addr = cpca._jieba_extract('我家的地址是江苏淮安清浦区人民路111号')

    assert addr == '我家的地址是江苏淮安清浦区人民路111号'
    assert pca.province == '江苏省'
    assert pca.province_pos == 6
    assert pca.city == '淮安市'
    assert pca.city_pos == 8
    assert pca.area == '清浦区'
    assert pca.area_pos == 10


def test_jieba_extract3(monkeypatch):
    """测试地名出现两次省名的情况"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省', '上海市': '上海市'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}))

    pca, addr = cpca._jieba_extract('我家的地址是江苏淮安清浦区人民路111号上海市')

    assert addr == '我家的地址是江苏淮安清浦区人民路111号上海市'
    assert pca.province == '江苏省'
    assert pca.province_pos == 6
    assert pca.city == '淮安市'
    assert pca.city_pos == 8
    assert pca.area == '清浦区'
    assert pca.area_pos == 10


def test_full_text_extract1(monkeypatch):
    """地址在开头"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}))

    pca, addr = cpca._full_text_extract('江苏淮安清浦区人民路111号', 8)

    assert addr == '人民路111号'
    assert pca.province == '江苏省'
    assert pca.province_pos == 0
    assert pca.city == '淮安市'
    assert pca.city_pos == 2
    assert pca.area == '清浦区'
    assert pca.area_pos == 4


def test_full_text_extract2(monkeypatch):
    """地址在结尾"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}))

    pca, addr = cpca._full_text_extract('我的家在江苏淮安清浦区', 8)

    assert addr == '我的家在江苏淮安清浦区'
    assert pca.province == '江苏省'
    assert pca.province_pos == 4
    assert pca.city == '淮安市'
    assert pca.city_pos == 6
    assert pca.area == '清浦区'
    assert pca.area_pos == 8


def test_full_text_extract3(monkeypatch):
    """地址在中间, 验证地址截取规则:只截取句子开头提取到的地址"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}))

    pca, addr = cpca._full_text_extract('我家的地址是江苏淮安清浦区人民路111号', 8)

    assert addr == '我家的地址是江苏淮安清浦区人民路111号'
    assert pca.province == '江苏省'
    assert pca.province_pos == 6
    assert pca.city == '淮安市'
    assert pca.city_pos == 8
    assert pca.area == '清浦区'
    assert pca.area_pos == 10    


def test_full_text_extract4(monkeypatch):
    """测试较小的lookahead"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}))

    pca, addr = cpca._full_text_extract('江苏淮安清浦区人民路111号', 2)

    assert addr == '清浦区人民路111号'
    assert pca.province == '江苏省'
    assert pca.province_pos == 0
    assert pca.city == '淮安市'
    assert pca.city_pos == 2
    assert pca.area == ''
    assert pca.area_pos == -1


def test_full_text_extract4(monkeypatch):
    """测试满足贪婪匹配模式"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省', '江苏省': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}))

    pca, addr = cpca._full_text_extract('江苏省淮安清浦区人民路111号', 3)

    assert addr == '人民路111号'
    assert pca.province == '江苏省'
    assert pca.province_pos == 0
    assert pca.city == '淮安市'
    assert pca.city_pos == 3
    assert pca.area == '清浦区'
    assert pca.area_pos == 5


def test_handle_one_record1(monkeypatch):
    """分词模式"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市', '淮安市': '淮安市'}, {'淮安市':'江苏省'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}, {'清浦区': '淮安市'}))

    result1 = cpca._handle_one_record("清浦区人民路111号", {}, True, 0, True)

    assert result1["省"] == '江苏省'
    assert result1['市'] == '淮安市'
    assert result1['区'] == '清浦区'
    assert result1['地址'] == '人民路111号'
    assert result1['省_pos'] == -1
    assert result1['市_pos'] == -1
    assert result1['区_pos'] == 0


def test_handle_one_record2(monkeypatch):
    """全文模式"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安': '淮安市', '淮安市': '淮安市'}, {'淮安市':'江苏省'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}, {'清浦区': '淮安市'}))

    result1 = cpca._handle_one_record("清浦区人民路111号", {}, False, 5, True)

    assert result1["省"] == '江苏省'
    assert result1['市'] == '淮安市'
    assert result1['区'] == '清浦区'
    assert result1['地址'] == '人民路111号'
    assert result1['省_pos'] == -1
    assert result1['市_pos'] == -1
    assert result1['区_pos'] == 0


def test_handle_one_record3(monkeypatch):
    """省区推断市的模式"""
    monkeypatch.setattr(cpca, 'province_map', {'江苏省': '江苏省'})
    monkeypatch.setattr(cpca, 'city_map', _dict2addr_map({'淮安市': '淮安市'}))
    monkeypatch.setattr(cpca, 'area_map', _dict2addr_map({'清浦区': '清浦区'}, is_unique_value=False))
    monkeypatch.setattr(cpca, 'province_area_map', _dict2addr_map({('江苏省', '清浦区'):''}, {('江苏省', '清浦区'):'淮安市'}))

    result1 = cpca._handle_one_record("江苏省清浦区人民路111号", {}, False, 5, True)

    assert result1["省"] == '江苏省'
    assert result1['市'] == '淮安市'
    assert result1['区'] == '清浦区'
    assert result1['地址'] == '人民路111号'
    assert result1['省_pos'] == 0
    assert result1['市_pos'] == -1
    assert result1['区_pos'] == 3
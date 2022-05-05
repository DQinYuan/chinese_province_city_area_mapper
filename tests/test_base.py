# -*- coding: utf-8 -*-

import sys

sys.path.append('..')
import addressparser
from addressparser.structures import Pca


def assert_addr(addr_df, pos_sensitive=False):
    def _assert_line(linenum, province, city, area, addr,
                     province_pos=-1, city_pos=-1, area_pos=-1):
        assert addr_df.loc[linenum, '省'] == province
        assert addr_df.loc[linenum, '市'] == city
        assert addr_df.loc[linenum, '区'] == area
        assert addr_df.loc[linenum, '地名'] == addr
        if pos_sensitive:
            assert addr_df.loc[linenum, '省_pos'] == province_pos
            assert addr_df.loc[linenum, '市_pos'] == city_pos
            assert addr_df.loc[linenum, '区_pos'] == area_pos

    _assert_line(0, '上海市', '上海市', '徐汇区', '虹漕路461号58号楼5楼', -1, -1, 0)
    _assert_line(1, '福建省', '泉州市', '洛江区', '万安塘西工业区', -1, 0, 3)
    _assert_line(2, '福建省', '福州市', '鼓楼区', '鼓楼医院', 0, -1, 3)
    _assert_line(3, '天津市', '天津市', '', '', 0, 0, -1)


def test_transform():
    """分词、全文测试"""
    addr_list = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "福建省鼓楼区鼓楼医院",
                 "天津市"]
    # 分词模式
    transed = addressparser.transform(addr_list, cut=True)
    print(transed)
    assert_addr(transed)

    # 全文匹配
    transed = addressparser.transform(addr_list, cut=False, pos_sensitive=True)
    print(transed)
    assert_addr(transed)

    # 分词匹配 测试pos_sensitive
    transed = addressparser.transform(addr_list, cut=True, pos_sensitive=True)
    print(transed)
    assert_addr(transed, pos_sensitive=True)


def test_data_from_csv():
    """测试数据加载"""
    area_map, city_map, province_area_map, province_map, latlng = addressparser._data_from_csv()
    print("....")
    assert province_map['北京'] == '北京市'
    assert city_map.get_full_name('北京') == '北京市'

    beijin_pca = [('北京市', '北京市', ''), ('北京市', '北京市', '东城区'), ('北京市', '北京市', '西城区'), ('北京市', '北京市', '朝阳区'),
                  ('北京市', '北京市', '丰台区'), ('北京市', '北京市', '石景山区'), ('北京市', '北京市', '海淀区'), ('北京市', '北京市', '门头沟区'),
                  ('北京市', '北京市', '房山区'), ('北京市', '北京市', '通州区'), ('北京市', '北京市', '顺义区'), ('北京市', '北京市', '昌平区'),
                  ('北京市', '北京市', '大兴区'), ('北京市', '北京市', '怀柔区'), ('北京市', '北京市', '平谷区'), ('北京市', '北京市', '密云区'),
                  ('北京市', '北京市', '延庆区')]
    assert set(city_map.get_relational_addrs('北京')) == set(beijin_pca)
    assert province_area_map.get_relational_addrs(('北京市', '东城区')) == [('北京市', '北京市', '东城区')]
    assert area_map.get_full_name('东城区') == '东城区'
    assert area_map.get_relational_addrs('东城区') == [('北京市', '北京市', '东城区')]
    assert latlng[('北京市', '北京市', '东城区')] is not None


def test_fill_province():
    pca = Pca('', '淮安市', '')
    addressparser._fill_province(pca)
    assert pca.province == "江苏省"
    assert pca.city == '淮安市'


def test_fill_city_1():
    pca = Pca('', '', '朝阳区')
    addressparser._fill_city(pca, {'朝阳区': '北京市'}, True)
    assert pca.city == '北京市'


def test_jieba_extract():
    """地址全部在句子开头的情况"""
    pca, addr = addressparser._jieba_extract('湖北武汉复兴路111号')
    print(pca, addr)
    assert addr == '复兴路111号'
    assert pca.province == '湖北省'
    assert pca.province_pos == 0
    assert pca.city == '武汉市'
    assert pca.city_pos == 2


def test_jieba_extract2():
    """地址在句子中间的情况"""
    pca, addr = addressparser._jieba_extract('我家的地址是湖北武汉武昌区复兴路111号')
    assert addr == '我家的地址是湖北武汉武昌区复兴路111号'
    assert pca.province == '湖北省'
    assert pca.province_pos == 6
    assert pca.city == '武汉市'
    assert pca.city_pos == 8
    assert pca.area == '武昌区'
    assert pca.area_pos == 10


def test_jieba_extract3():
    """测试地名出现两次省名的情况"""
    pca, addr = addressparser._jieba_extract('我家的地址是湖北武汉武昌区复兴路111号上海市')
    assert addr == '我家的地址是湖北武汉武昌区复兴路111号上海市'
    assert pca.province == '湖北省'
    assert pca.province_pos == 6
    assert pca.city == '武汉市'
    assert pca.city_pos == 8
    assert pca.area == '武昌区'
    assert pca.area_pos == 10


def test_full_text_extract0():
    """地址在开头"""
    pca, addr = addressparser._full_text_extract('湖北省武汉武昌区复兴路111号', 8)
    print(pca, addr)
    assert addr == '复兴路111号'
    assert pca.province == '湖北省'
    assert pca.province_pos == 0
    assert pca.city == '武汉市'
    assert pca.city_pos == 3
    assert pca.area == '武昌区'
    assert pca.area_pos == 5


def test_full_text_extract1():
    """地址在开头"""
    pca, addr = addressparser._full_text_extract('湖北武汉武昌区复兴路111号', 8)
    print(pca, addr)
    assert addr == '复兴路111号'
    assert pca.province == '湖北省'
    assert pca.province_pos == 0
    assert pca.city == '武汉市'
    assert pca.city_pos == 2
    assert pca.area == '武昌区'
    assert pca.area_pos == 4


def test_full_text_extract2():
    """地址在结尾"""
    pca, addr = addressparser._full_text_extract('我的家在湖北武汉武昌区', 8)
    print(pca, addr)
    assert addr == '我的家在湖北武汉武昌区'
    assert pca.province == '湖北省'
    assert pca.province_pos == 4
    assert pca.city == '武汉市'
    assert pca.city_pos == 6
    assert pca.area == '武昌区'
    assert pca.area_pos == 8


def test_full_text_extract3():
    """地址在中间, 验证地址截取规则:只截取句子开头提取到的地址"""
    pca, addr = addressparser._full_text_extract('我家的地址是湖北武汉武昌区复兴路1号', 8)
    print(pca, addr)
    assert addr == '我家的地址是湖北武汉武昌区复兴路1号'
    assert pca.province == '湖北省'
    assert pca.province_pos == 6
    assert pca.city == '武汉市'
    assert pca.city_pos == 8
    assert pca.area == '武昌区'
    assert pca.area_pos == 10


def test_full_text_extract4():
    """测试较小的lookahead"""
    pca, addr = addressparser._full_text_extract('湖北武汉东西湖区复兴路1号', 2)
    print(pca, addr)
    assert addr == '东西湖区复兴路1号'
    assert pca.province == '湖北省'
    assert pca.province_pos == 0
    assert pca.city == '武汉市'
    assert pca.city_pos == 2
    assert pca.area == ''
    assert pca.area_pos == -1


def test_full_text_extract5():
    """测试满足贪婪匹配模式"""
    pca, addr = addressparser._full_text_extract('湖北武汉武昌区复兴路1号', 3)
    print(pca, addr)
    assert addr == '复兴路1号'
    assert pca.province == '湖北省'
    assert pca.province_pos == 0
    assert pca.city == '武汉市'
    assert pca.city_pos == 2
    assert pca.area == '武昌区'
    assert pca.area_pos == 4


def test_full_text_extract6():
    """地址在开头 4级地址测试"""
    pca, addr = addressparser._full_text_extract('泉州市洛江区万安塘西工业区', 8)
    print(pca, addr)
    assert addr == '万安塘西工业区'
    assert pca.province_pos == -1
    assert pca.city == '泉州市'
    assert pca.city_pos == 0
    assert pca.area == '洛江区'
    assert pca.area_pos == 3


def test_handle_one_record1():
    """分词模式"""
    result1 = addressparser._handle_one_record("江苏淮安市人民路111号", {}, True, 0, True, True)
    print(result1)
    assert result1["省"] == '江苏省'
    assert result1['市'] == '淮安市'
    assert result1['区'] == ''
    assert result1['地名'] == '人民路111号'
    assert result1['省_pos'] == 0
    assert result1['市_pos'] == 2
    assert result1['区_pos'] == -1


def test_handle_one_record2():
    """全文模式"""
    result1 = addressparser._handle_one_record("江苏淮安市人民路111号", {}, False, 5, True, True)
    print(result1)
    assert result1["省"] == '江苏省'
    assert result1['市'] == '淮安市'
    assert result1['区'] == ''
    assert result1['地名'] == '人民路111号'
    assert result1['省_pos'] == 0
    assert result1['市_pos'] == 2
    assert result1['区_pos'] == -1


def test_handle_one_record3():
    """省区推断市的模式"""
    result1 = addressparser._handle_one_record("江苏省清江浦区人民路111号", {}, False, 5, True, True)

    assert result1["省"] == '江苏省'
    assert result1['市'] == '淮安市'
    assert result1['区'] == '清江浦区'
    assert result1['地名'] == '人民路111号'
    assert result1['省_pos'] == 0
    assert result1['市_pos'] == -1
    assert result1['区_pos'] == 3

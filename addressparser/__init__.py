# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description:
"""

import os
import six
import warnings
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
import pandas as pd

from .structures import AddrMap, Pca
from .structures import P, C, A

__version__ = "0.2.4"

pwd_path = os.path.abspath(os.path.dirname(__file__))
# 区划地址文件
pca_path = os.path.join(pwd_path, 'pca.csv')

if six.PY2:
    text_type = unicode
else:
    text_type = str


def convert_to_unicode(text):
    """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
    if not isinstance(text, text_type):
        try:
            text = text.decode('utf-8')
        except UnicodeDecodeError:
            text = text.decode('gbk', 'ignore')
        except Exception as e:
            warnings.warn('Convert to unicode error: %s, text: %s' % (e, text))
    return text


def _data_from_csv():
    """
    从csv文件获取数据
    :return: (AddrMap, AddrMap, AddrMap, dict, dict)
    """
    # 区名及其简写 -> 相关pca元组
    area_map = AddrMap()
    # 城市名及其简写 -> 相关pca元组
    city_map = AddrMap()
    # (省名全称, 区名全称) -> 相关pca元组
    province_area_map = AddrMap()
    # 省名 -> 省全名
    province_map = {}
    # (省名, 市名, 区名) -> (纬度,经度)
    latlng = {}
    # 数据约定:国家直辖市的sheng字段为直辖市名称, 省直辖县的city字段为空

    pca_df = pd.read_csv(pca_path, sep=',', header=0, encoding='utf-8')
    pca_df = pca_df.fillna('')
    for record_dict in pca_df.values:
        # latlng[(record_dict['sheng'], record_dict['shi'], record_dict['qu'])] =
        # (record_dict['lat'], record_dict['lng'])
        record_dict = [convert_to_unicode(i) if i is isinstance(i, text_type) else i for i in record_dict]
        latlng[(record_dict[1], record_dict[2], record_dict[3])] = (record_dict[4], record_dict[5])

        _fill_province_map(province_map, record_dict)
        _fill_area_map(area_map, record_dict)
        _fill_city_map(city_map, record_dict)
        _fill_province_area_map(province_area_map, record_dict)

    return area_map, city_map, province_area_map, province_map, latlng


def _fill_province_area_map(province_area_map, record_dict):
    """
    填充省，区
    :param province_area_map: AddrMap
    :param record_dict:
    :return:
    """
    pca_tuple = (record_dict[1], record_dict[2], record_dict[3])
    key = (record_dict[1], record_dict[3])
    # 第三个参数在此处没有意义
    province_area_map.append_relational_addr(key, pca_tuple, P)


# 过滤混淆区名 '河北北戴河富丽小区1号'
filter_area_names = [u'河北区', u'新城区']
# 处理了部分常见自治县简写
short_area_names = {
    u'白沙黎族自治县': u'白沙县',
    u'昌江黎族自治县': u'昌江县',
    u'乐东黎族自治县': u'乐东县',
    u'陵水黎族自治县': u'陵水县',
    u'保亭黎族苗族自治县': u'保亭县',
    u'琼中黎族苗族自治县': u'琼中县',
    u'长阳土家族自治县': u'长阳县',
    u'五峰土家族自治县': u'五峰县',
    u'大通回族土族自治县': u'大通县',
    u'民和回族土族自治县': u'民和县',
    u'互助土族自治县': u'互助县',
    u'化隆回族自治县': u'化隆县',
    u'循化撒拉族自治县': u'循化县',
    u'青龙满族自治县': u'青龙县',
    u'屏边苗族自治县': u'屏边县',
    u'金平苗族瑶族傣族自治县': u'金平县',
    u'河口瑶族自治县': u'河口县',
    u'丰宁满族自治县': u'丰宁县',
    u'宽城满族自治县': u'宽城县',
    u'围场满族蒙古族自治县': u'围场县',
}


def _fill_area_map(area_map, record_dict):
    """
    填充三级区划（区级）地名，包括简称
    :param area_map:  AddrMap, dict
    :param record_dict: dict
    :return: area_map
    """
    area_name = record_dict[3]
    pca_tuple = (record_dict[1], record_dict[2], record_dict[3])
    area_map.append_relational_addr(area_name, pca_tuple, A)
    # 自治县区划简称
    if area_name in short_area_names.keys():
        area_map.append_relational_addr(short_area_names[area_name], pca_tuple, A)
    # 4字区划简称
    elif len(area_name) > 3 and (area_name.endswith(u'新区') or area_name.endswith(u'城区') or area_name.endswith(u'林区')):
        area_map.append_relational_addr(area_name[:-2], pca_tuple, A)
    # 过滤的区划名称
    elif area_name in filter_area_names:
        pass
    # 3字区划简称，'XX区'不简写
    elif len(area_name) > 2 and (area_name.endswith(u'市') or area_name.endswith(u'县')):
        area_map.append_relational_addr(area_name[:-1], pca_tuple, A)


# 过滤混淆市名 eg '吉林省、吉林市的混淆'
filter_city_names = [u'吉林市']


def _fill_city_map(city_map, record_dict):
    """
    填充二级区划（市级）地名，包括简称
    :param city_map: AddrMap, dict
    :param record_dict: dict
    :return: city_map
    """
    city_name = record_dict[2]  # shi
    pca_tuple = (record_dict[1], record_dict[2], record_dict[3])
    city_map.append_relational_addr(city_name, pca_tuple, C)
    # fix 吉林省、吉林市的混淆
    if city_name in filter_city_names:
        pass
    elif city_name.endswith(u'市'):
        city_map.append_relational_addr(city_name[:-1], pca_tuple, C)
    # 特别行政区
    # elif city_name == u'香港特别行政区':
    #     city_map.append_relational_addr(u'香港', pca_tuple, C)
    # elif city_name == u'澳门特别行政区':
    #     city_map.append_relational_addr(u'澳门', pca_tuple, C)
    # 自治区下的二级区划，eg喀什地区
    elif len(city_name) > 3 and city_name.endswith(u'地区'):
        city_map.append_relational_addr(city_name[:-2], pca_tuple, C)


def _fill_province_map(province_map, record_dict):
    """
    填充一级区划（省级）地名，包括简称
    :param province_map: dict
    :param record_dict: dict
    :return: province_map
    """
    sheng = record_dict[1]  # sheng
    if sheng not in province_map:
        province_map[sheng] = sheng
        # 处理省的简写情况
        # 普通省分 和 直辖市
        if sheng.endswith(u'省') or sheng.endswith(u'市'):
            province_map[sheng[:-1]] = sheng
        # 自治区
        elif sheng == u'新疆维吾尔自治区':
            province_map[u'新疆'] = sheng
        elif sheng == u'内蒙古自治区':
            province_map['内蒙古'] = sheng
        elif sheng == u'广西壮族自治区':
            province_map[u'广西'] = sheng
            province_map[u'广西省'] = sheng
        elif sheng == u'西藏自治区':
            province_map[u'西藏'] = sheng
        elif sheng == u'宁夏回族自治区':
            province_map[u'宁夏'] = sheng
        # 特别行政区
        elif sheng == u'香港特别行政区':
            province_map[u'香港'] = sheng
        elif sheng == u'澳门特别行政区':
            province_map[u'澳门'] = sheng


area_map, city_map, province_area_map, province_map, latlng = _data_from_csv()

# 直辖市
munis = {u'北京市', u'天津市', u'上海市', u'重庆市'}


def is_munis(city_full_name):
    return city_full_name in munis


# 区级到市级的映射
myumap = {
    u'南关区': u'长春市',
    u'南山区': u'深圳市',
    u'宝山区': u'上海市',
    u'普陀区': u'上海市',
    u'浦东区': u'上海市',
    u'市辖区': u'东莞市',
    u'朝阳区': u'北京市',
    u'河东区': u'天津市',
    u'白云区': u'广州市',
    u'西湖区': u'杭州市',
    u'铁西区': u'沈阳市',
}


def transform(location_strs, umap=myumap, index=[], cut=False, lookahead=8, pos_sensitive=False, open_warning=False):
    """将地址描述字符串转换以"省","市","区"信息为列的DataFrame表格
        Args:
            locations:地址描述字符集合,可以是list, Series等任意可以进行for in循环的集合
                      比如:["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            umap:自定义的区级到市级的映射,主要用于解决区重名问题,如果定义的映射在模块中已经存在，则会覆盖模块中自带的映射
            index:可以通过这个参数指定输出的DataFrame的index,默认情况下是range(len(data))
            cut:是否使用分词，默认使用，分词模式速度较快，但是准确率可能会有所下降
            lookahead:只有在cut为false的时候有效，表示最多允许向前看的字符的数量
                      默认值为8是为了能够发现"新疆维吾尔族自治区"这样的长地名
                      如果你的样本中都是短地名的话，可以考虑把这个数字调小一点以提高性能
            pos_sensitive:如果为True则会多返回三列，分别提取出的省市区在字符串中的位置，如果字符串中不存在的话则显示-1
            open_warning: 是否打开umap警告, 默认关闭
        Returns:
            一个Pandas的DataFrame类型的表格，如下：
               |省    |市   |区    |地名                 |
               |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
               |福建省|泉州市|洛江区|万安塘西工业区        |
    """
    if not isinstance(location_strs, Iterable):
        from .exceptions import InputTypeNotSuportException
        raise InputTypeNotSuportException(
            'location_strs参数必须为可迭代的类型(比如list, Series等实现了__iter__方法的对象)')

    result = pd.DataFrame(
        [_handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning) for addr in location_strs],
        index=index) \
        if index else pd.DataFrame(
        [_handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning) for addr in location_strs])
    # 这句的唯一作用是让列的顺序好看一些
    if pos_sensitive:
        return result.loc[:, ('省', '市', '区', '地名', '省_pos', '市_pos', '区_pos')]
    else:
        return result.loc[:, ('省', '市', '区', '地名')]


def _handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning):
    """处理一条记录"""
    addr = convert_to_unicode(addr)
    # 空记录
    if not addr or not isinstance(addr, text_type):
        empty = {'省': '', '市': '', '区': ''}
        if pos_sensitive:
            empty['省_pos'] = -1
            empty['市_pos'] = -1
            empty['区_pos'] = -1
        return empty

    # 地名提取
    pca, left_addr = _extract_addr(addr, cut, lookahead)
    # 填充市
    _fill_city(pca, umap, open_warning)
    # 填充省
    _fill_province(pca)

    result = pca.propertys_dict(pos_sensitive)
    result['地名'] = left_addr
    return result


def _fill_province(pca):
    """填充省"""
    if (not pca.province) and pca.city and (pca.city in city_map):
        pca.province = city_map.get_value(pca.city, P)


def _fill_city(pca, umap, open_warning):
    """填充市"""
    if not pca.city:
        # 从 区 映射
        if pca.area:
            # 从umap中映射
            if umap.get(pca.area):
                pca.city = umap.get(pca.area)
                return
            if pca.area in area_map and area_map.is_unique_value(pca.area):
                if pca.province:
                    if area_map.get_value(pca.area, P) == pca.province:
                        pca.city = area_map.get_value(pca.area, C)
                        return
                else:
                    pca.city = area_map.get_value(pca.area, C)
                    return

        # 从 省,区 映射
        if pca.area and pca.province:
            newKey = (pca.province, pca.area)
            if newKey in province_area_map and province_area_map.is_unique_value(newKey):
                pca.city = province_area_map.get_value(newKey, C)
                return

        if open_warning:
            warnings.warn("%s 无法映射, 建议添加进umap中" % pca.area)


def _extract_addr(addr, cut, lookahead):
    """提取地址中的省,市,区名称
       Args:
           addr:原始地址字符串
           cut: 是否分词
       Returns:
           [sheng, shi, qu, (sheng_pos, shi_pos, qu_pos)], addr
    """
    return _jieba_extract(addr) if cut else _full_text_extract(addr, lookahead)


def _jieba_extract(addr):
    """基于结巴分词进行提取"""
    import jieba
    result = Pca()
    pos = 0
    truncate = {0: 0}

    def _set_pca(pca_property, name, full_name):
        """pca_property: 'province', 'city' or 'area'"""
        if not getattr(result, pca_property):
            setattr(result, pca_property, full_name)
            setattr(result, pca_property + "_pos", pos)
            if is_munis(full_name):
                setattr(result, "province_pos", pos)
            # nonlocal truncate, replace with dict
            # refer: https://www.it610.com/article/50433.htm
            if pos == truncate[0]:
                truncate[0] += len(name)

    for word in jieba.cut(addr):
        # 优先提取低级别行政区 (主要是为直辖市和特别行政区考虑)
        if word in area_map:
            _set_pca('area', word, area_map.get_full_name(word))
        elif word in city_map:
            _set_pca('city', word, city_map.get_full_name(word))
        elif word in province_map:
            _set_pca('province', word, province_map[word])

        pos += len(word)

    return result, addr[truncate[0]:]


filter_address_chars = [u'路', u'街', u'村', u'桥']


def _full_text_extract(addr, lookahead):
    """全文匹配进行提取"""
    result = Pca()
    truncate = {0: 0}

    def _set_pca(pca_property, pos, name, full_name):
        """pca_property: 'province', 'city' or 'area'"""

        def _defer_set():
            if not getattr(result, pca_property):
                setattr(result, pca_property, full_name)
                setattr(result, pca_property + "_pos", pos)
                if is_munis(full_name):
                    setattr(result, "province_pos", pos)
                # nonlocal truncate
                if pos == truncate[0]:
                    truncate[0] += len(name)
            return len(name)

        return _defer_set

    # i为起始位置
    i = 0
    while i < len(addr):
        # 用于设置pca属性的函数
        defer_fun = None
        # length为从起始位置开始的长度,从中提取出最长的地址
        for length in range(1, lookahead + 1):
            end_pos = i + length
            if end_pos > len(addr):
                break
            word = addr[i:end_pos]
            word_next = addr[end_pos] if end_pos < len(addr) else ''

            # 优先提取低级别的行政区 (主要是为直辖市和特别行政区考虑)
            if word_next in filter_address_chars:
                continue
            elif word in area_map:
                defer_fun = _set_pca('area', i, word, area_map.get_full_name(word))
                continue
            elif word in city_map:
                defer_fun = _set_pca('city', i, word, city_map.get_full_name(word))
                continue
            elif word in province_map:
                defer_fun = _set_pca('province', i, word, province_map[word])
                continue

        if defer_fun:
            i += defer_fun()
        else:
            i += 1

    return result, addr[truncate[0]:]

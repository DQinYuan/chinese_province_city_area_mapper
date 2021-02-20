# -*- coding: utf-8 -*-
# __init__.py


from .structures import AddrMap, Pca
from .structures import P, C, A
from .matcher import Matcher

VERSION = (0, 5, 4)

__version__ = ".".join([str(x) for x in VERSION])

# 结果 dataframe 的列名
_PROVINCE = "省"
_PROVINCE_POS = "省_pos"

_CITY = "市"
_CITY_POS = "市_pos"

_COUNTY = "区"
_COUNTY_POS = "区_pos"

_ADDR = "地址"

_ADCODE = "adcode"

_POS_KEY = {
    _PROVINCE: _PROVINCE_POS,
    _CITY: _CITY_POS,
    _COUNTY: _COUNTY_POS
}

rank2name = [_PROVINCE, _CITY, _COUNTY]
rank2pos_key = [_PROVINCE_POS, _CITY_POS, _COUNTY_POS]


class AddrInfo:

    RANK_PROVINCE = 0
    RANK_CITY = 1
    RANK_COUNTY = 2

    def __init__(self, name, adcode, longitude, latitude) -> None:
        self.name = name
        # adcode 的前 6 位代表省市区三级
        self.adcode = adcode[:6]
        self.longitude = longitude
        self.latitude = latitude

        # rank 代表行政区划级别 0: 省 1: 市 2: 县
        if self.adcode.endswith("0000"):
            self.rank = AddrInfo.RANK_PROVINCE
        elif self.adcode.endswith("00"):
            self.rank = AddrInfo.RANK_CITY
        else:
            self.rank = AddrInfo.RANK_COUNTY

    def belong_to(self, other):
        """通过 adcode 判断当前 addr 是否属于 other"""
        return self.adcode.startswith(other.adcode[:(other.rank+1) * 2])


# 停用词包括: 省, 市, 特别行政区, 自治区.
# 之所以 区 和 县 不作为停用词，是因为 区县 数目太多, 去掉 "区" 字 或者 "县" 字后很容易误配
def _init_data(stop_key="([省市]|特别行政区|自治区)$") -> (dict, Matcher):
    ad_map = {}
    matcher = Matcher(stop_key)
    from pkg_resources import resource_stream
    with resource_stream('cpca.resources', 'adcodes.csv') as csv_stream:
        from io import TextIOWrapper
        import csv
        text = TextIOWrapper(csv_stream, encoding='utf8')
        adcodes_csv_reader = csv.DictReader(text)
        for record_dict in adcodes_csv_reader:
            addr_info = AddrInfo(
                name=record_dict["name"],
                adcode=record_dict["adcode"],
                longitude=record_dict["longitude"],
                latitude=record_dict["latitude"])
            ad_map[record_dict["adcode"]] = addr_info
            matcher.add_addr_info(addr_info)
    matcher.complete_add()

    return ad_map, matcher


ad_2_addr_dict, matcher = _init_data()


def transform(location_strs, index=None, pos_sensitive=False, umap={}):
    """将地址描述字符串转换以"省","市","区"信息为列的DataFrame表格
        Args:
            locations:地址描述字符集合,可以是list, Series等任意可以进行for in循环的集合
                      比如:["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            index:可以通过这个参数指定输出的DataFrame的index,默认情况下是range(len(data))
            pos_sensitive:如果为True则会多返回三列，分别提取出的省市区在字符串中的位置，如果字符串中不存在的话则显示-1
            umap: 当只有区的信息时， 且该区存在同名时， 指定该区具体是哪一个，字典的 key 为区名，value 为 adcode， 比如 {"朝阳区": "110105"}
        Returns:
            一个Pandas的DataFrame类型的表格，如下：
               |省    |市   |区    |地址                 |adcode   |
               |上海市|市辖区|徐汇区|虹漕路461号58号楼5楼   |310104 |
               |福建省|泉州市|洛江区|万安塘西工业区        |350504 |
    """
    from collections.abc import Iterable

    if not isinstance(location_strs, Iterable):
        from .exceptions import InputTypeNotSuportException
        raise InputTypeNotSuportException(
            'location_strs参数必须为可迭代的类型(比如list, Series等实现了__iter__方法的对象)')

    import pandas as pd
    result = pd.DataFrame(
             [_get_one_addr(sentence, pos_sensitive, umap) for sentence in location_strs],
             index=index)

    return tidy_order(result, pos_sensitive)


def transform_text_with_addrs(text_with_addrs, index=None, pos_sensitive=False, umap={}):
    """将含有多个地址的长文本中的地址全部提取出来
         Args:
             text_with_addrs: 一个字符串，里面可能含有多个地址
             index:可以通过这个参数指定输出的DataFrame的index,默认情况下是range(len(data))
             pos_sensitive:如果为True则会多返回三列，分别提取出的省市区在字符串中的位置，如果字符串中不存在的话则显示-1
             umap: 当只有区的信息时， 且该区存在同名时， 指定该区具体是哪一个，字典的 key 为区名，value 为 adcode， 比如 {"朝阳区": "110105"}
    """
    import pandas as pd
    result = pd.DataFrame(_extract_addrs(text_with_addrs, pos_sensitive, umap, truncate_pos=False,
                                         new_entry_when_not_belong=True),
                          index=index)
    return tidy_order(result, pos_sensitive)


def tidy_order(df, pos_sensitive):
    """整理顺序,唯一作用是让列的顺序好看一些"""
    if pos_sensitive:
        return df.loc[:, (_PROVINCE, _CITY, _COUNTY, _ADDR, _ADCODE, _PROVINCE_POS, _CITY_POS,
                              _COUNTY_POS)]
    else:
        return df.loc[:, (_PROVINCE, _CITY, _COUNTY, _ADDR, _ADCODE)]


class MatchInfo:

    def __init__(self, attr_infos, start_index, end_index) -> None:
        self.attr_infos = attr_infos
        self.start_index = start_index
        self.end_index = end_index


def empty_record(pos_sensitive: bool):
    empty = {_PROVINCE: None, _CITY: None, _COUNTY: None, _ADDR: None, _ADCODE: None}
    if pos_sensitive:
        empty[_PROVINCE_POS] = -1
        empty[_CITY_POS] = -1
        empty[_COUNTY_POS] = -1
    return empty


def pos_setter(pos_sensitive):
    def set_pos(res, rank, pos):
        res[rank2pos_key[rank]] = pos

    def empty(res, rank, pos): pass
    return set_pos if pos_sensitive else empty


def _get_one_addr(sentence, pos_sensitive, umap):
    return next(_extract_addrs(sentence, pos_sensitive, umap))


def _extract_addrs(sentence, pos_sensitive, umap, truncate_pos=True, new_entry_when_not_belong=False) -> dict:
    """提取出 sentence 中的所有地址"""
    # 空记录
    if not isinstance(sentence, str) or sentence == '' or sentence is None:
        yield empty_record(pos_sensitive)
        return

    set_pos = pos_setter(pos_sensitive)

    # 从大地区向小地区匹配
    res = empty_record(pos_sensitive)
    last_info = None
    adcode = None
    truncate_index = -1
    for match_info in matcher.iter(sentence):
        # 当没有省市等上级地区限制时, 优先选择的区的 adcode
        first_adcode = umap.get(match_info.origin_value)
        cur_addr = match_info.get_match_addr(last_info, first_adcode)
        if cur_addr:
            set_pos(res, match_info.get_rank(), match_info.start_index)
            last_info = cur_addr
            adcode = cur_addr.adcode
            truncate_index = match_info.end_index
            # 匹配到了县级就停止
            if cur_addr.rank == AddrInfo.RANK_COUNTY:
                update_res_by_adcode(res, adcode)
                res[_ADDR] = sentence[truncate_index + 1:] if truncate_pos else ""
                res[_ADCODE] = adcode
                yield res
                res = empty_record(pos_sensitive)
                last_info = None
                adcode = None
                truncate_index = -1
        elif new_entry_when_not_belong:
            # 当找不到可以匹配的地址时,新建新的数据项
            update_res_by_adcode(res, adcode)
            res[_ADDR] = sentence[truncate_index + 1:] if truncate_pos else ""
            res[_ADCODE] = adcode
            yield res
            addr = match_info.get_match_addr(None, first_adcode)
            res = empty_record(pos_sensitive)
            set_pos(res, match_info.get_rank(), match_info.start_index)
            last_info = addr
            adcode = addr.adcode
            truncate_index = match_info.end_index

    if adcode is None:
        yield res
        return

    update_res_by_adcode(res, adcode)
    res[_ADDR] = sentence[truncate_index + 1:] if truncate_pos else ""
    res[_ADCODE] = adcode
    yield res


def _fill_adcode(adcode):
    return '{:0<12s}'.format(adcode)


def adcode_name(part_adcode: str):
    addr = ad_2_addr_dict.get(_fill_adcode(part_adcode))
    return None if addr is None else addr.name


def update_res_by_adcode(res: dict, adcode: str):
    if adcode.endswith("0000"):
        res[_PROVINCE] = adcode_name(adcode[:2])
        return
    if adcode.endswith("00"):
        res[_PROVINCE] = adcode_name(adcode[:2])
        res[_CITY] = adcode_name(adcode[:4])
        return
    res[_PROVINCE] = adcode_name(adcode[:2])
    res[_CITY] = adcode_name(adcode[:4])
    res[_COUNTY] = adcode_name(adcode)

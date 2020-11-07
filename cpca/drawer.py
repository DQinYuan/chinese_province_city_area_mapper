# -*- coding: utf-8 -*-
from . import ad_2_addr_dict
from . import _fill_adcode
from collections import defaultdict
import itertools
import operator


def ad2addr(part_adcode):
    return ad_2_addr_dict[_fill_adcode(part_adcode)]


def _base_input_check(locations):
    import pandas as pd
    from .exceptions import InputTypeNotSuportException
    if not isinstance(locations, pd.DataFrame):
        raise InputTypeNotSuportException(InputTypeNotSuportException.input_type)
    if "省" not in locations.columns or "市" not in locations.columns \
            or "区" not in locations.columns:
        raise InputTypeNotSuportException(InputTypeNotSuportException.input_type)


def _geo_update(geo, adcodes):
    coordinates = {}
    rest_adcodes = []
    for adcode in adcodes:
        if not ad2addr(adcode).longitude or not ad2addr(adcode).latitude:
            continue
        coordinates[adcode] = (float(ad2addr(adcode).longitude), float(ad2addr(adcode).latitude))
        rest_adcodes.append(adcode)
    geo._coordinates = coordinates
    return rest_adcodes


def draw_locations(adcodes, file_path):
    """
    基于folium生成地域分布的热力图的html文件.
    :param adcodes: 地址集
    :param file_path: 生成的html文件的路径.
    """
    import folium
    from folium.plugins import HeatMap
    adcodes = filter(None, adcodes)

    # 注意判断key是否存在
    heatData = []
    for adcode in adcodes:
        attr_info = ad2addr(adcode)
        if not attr_info.latitude or not attr_info.longitude:
            continue
        heatData.append([float(attr_info.latitude), float(attr_info.longitude), 1])
    # 绘制Map，开始缩放程度是5倍
    map_osm = folium.Map(location=[35, 110], zoom_start=5)
    # 将热力图添加到前面建立的map里
    HeatMap(heatData).add_to(map_osm)
    # 保存为html文件
    map_osm.save(file_path)


def echarts_draw(adcodes, file_path, title="地域分布图"
                 , subtitle="location distribute"):
    """
    生成地域分布的echarts热力图的html文件.
    :param adcodes: 地址集
    :param file_path: 生成的html文件路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    """
    from pyecharts import Geo


    # 过滤 None
    # 过滤掉缺乏经纬度数据的地点
    coordinates = {}
    counter = defaultdict(int)
    for adcode in filter(None, adcodes):
        addr = ad2addr(adcode)
        if not addr.longitude or not addr.latitude:
            continue
        counter[adcode] = counter[adcode] + 1
        coordinates[adcode] = (float(addr.longitude), float(addr.latitude))

    geo = Geo(title, subtitle, title_color="#fff",
              title_pos="center", width=1200,
              height=600, background_color='#404a59')
    geo._coordinates = coordinates

    attr, value = geo.cast(counter)
    geo.add("", attr, value, type="heatmap", is_visualmap=True,
            visual_text_color='#fff',
            is_piecewise=True, visual_split_number=10)
    geo.render(file_path)


def echarts_cate_draw(adcodes, labels, file_path, title="地域分布图", subtitle="location distribute",
                      point_size=7):
    """
    依据分类生成地域分布的echarts散点图的html文件.
    :param adcodes: 地址集
    :param labels: 长度必须和locations相等, 代表每个样本所属的分类.
    :param file_path: 生成的html文件路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    :param point_size: 每个散点的大小
    """

    if len(adcodes) != len(labels):
        from .exceptions import CPCAException
        raise CPCAException("locations的长度与labels长度必须相等")

    # 过滤 None
    # 过滤掉缺乏经纬度数据的地点
    coordinates = {}
    tuples = []
    for adcode, label in filter(lambda t: t[0] is not None, zip(adcodes, labels)):
        addr = ad2addr(adcode)
        if not addr.longitude or not addr.latitude:
            continue
        coordinates[adcode] = (float(addr.longitude), float(addr.latitude))
        tuples.append((adcode, label))

    from pyecharts import Geo
    geo = Geo(title, subtitle, title_color="#000000",
              title_pos="center", width=1200,
              height=600, background_color='#fff')
    geo._coordinates = coordinates

    for label, sub_tuples in itertools.groupby(tuples, operator.itemgetter(1)):
        sub_adcodes_list = list(map(operator.itemgetter(0), sub_tuples))
        value = [1] * len(sub_adcodes_list)
        geo.add(label, sub_adcodes_list, value, symbol_size=point_size,
                legend_pos="left", legend_top="bottom",
                geo_normal_color="#fff",
                geo_emphasis_color=" #f0f0f5")

    geo.render(file_path)

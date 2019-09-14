# -*- coding: utf-8 -*-
from . import latlng


def _base_input_check(locations):
    import pandas as pd
    from .exceptions import InputTypeNotSuportException
    if not isinstance(locations, pd.DataFrame):
        raise InputTypeNotSuportException(InputTypeNotSuportException.input_type)
    if "省" not in locations.columns or "市" not in locations.columns \
         or "区" not in locations.columns:
        raise InputTypeNotSuportException(InputTypeNotSuportException.input_type)


_lnglat = dict([(item[0], tuple(reversed(item[1]))) for item in latlng.items()])


def _geo_update(geo):
    geo._coordinates = _lnglat


def draw_locations(locations, file_path):
    """
    基于folium生成地域分布的热力图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param file_path: 生成的html文件的路径.
    """
    _base_input_check(locations)
    import folium
    from folium.plugins import HeatMap
    # 注意判断key是否存在
    heatData = []
    for map_key in zip(locations["省"], locations["市"], locations["区"]):
        if latlng.get(map_key):
            lat_lon = latlng.get(map_key)
            heatData.append([float(lat_lon[0]), float(lat_lon[1]), 1])
    # 绘制Map，开始缩放程度是5倍
    map_osm = folium.Map(location=[35, 110], zoom_start=5)
    # 将热力图添加到前面建立的map里
    HeatMap(heatData).add_to(map_osm)
    # 保存为html文件
    map_osm.save(file_path)


def echarts_draw(locations, file_path, title="地域分布图"
                 , subtitle="location distribute"):
    """
    生成地域分布的echarts热力图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param file_path: 生成的html文件路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    """
    from pyecharts import Geo

    _base_input_check(locations)
    count_map = {}
    for map_key in zip(locations["省"], locations["市"], locations["区"]):
        if latlng.get(map_key):
            count_map[map_key] = count_map.get(map_key, 0) + 1

    geo = Geo(title, subtitle, title_color="#fff",
          title_pos="center", width=1200,
          height=600, background_color='#404a59')
    _geo_update(geo)
    attr, value = geo.cast(count_map)
    geo.add("", attr, value, type="heatmap", is_visualmap=True,
        visual_text_color='#fff',
        is_piecewise=True, visual_split_number=10)
    geo.render(file_path)


def echarts_cate_draw(locations, labels, file_path, title="地域分布图", subtitle="location distribute",
                      point_size=7):
    """
    依据分类生成地域分布的echarts散点图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param labels: 长度必须和locations相等, 代表每个样本所属的分类.
    :param file_path: 生成的html文件路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    :param point_size: 每个散点的大小
    """
    _base_input_check(locations)
    
    if len(locations) != len(labels):
        from .exceptions import CPCAException
        raise CPCAException("locations的长度与labels长度必须相等")

    from pyecharts import Geo
    
    geo = Geo(title, subtitle, title_color="#000000",
          title_pos="center", width=1200,
          height=600, background_color='#fff')
    _geo_update(geo)
    
    uniques = set(list(labels))
    

    def _data_add(_geo, _cate_keys, _category):
        real_keys = []
        for cate_key in _cate_keys:
            if latlng.get(cate_key):
                real_keys.append(cate_key)
        
        attr = real_keys
        value = [1] * len(real_keys)
        geo.add(_category, attr, value, symbol_size=point_size,
                legend_pos="left", legend_top="bottom", 
                geo_normal_color="#fff",
                geo_emphasis_color =" #f0f0f5")
    
    for category in uniques:
        cate_locations = locations[labels == category]
        _data_add(geo, zip(cate_locations["省"], cate_locations["市"],
                           cate_locations["区"]), category)
        
    geo.render(file_path)

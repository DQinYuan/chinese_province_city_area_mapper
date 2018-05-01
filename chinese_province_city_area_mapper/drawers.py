# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 13:38:00 2018

@author: 燃烧杯
"""

def _base_input_check(locations):
    import pandas as pd
    from .exceptions import InputTypeNotSuportException
    if not isinstance(locations, pd.DataFrame):
        raise InputTypeNotSuportException(InputTypeNotSuportException.input_type)
    if "省" not in locations.columns or "市" not in locations.columns \
         or "区" not in locations.columns:
        raise InputTypeNotSuportException(InputTypeNotSuportException.input_type)
        
def _geo_update(geo):
    from .mappers import lon_lat_mapper
    geo._coordinates.update(lon_lat_mapper)


def draw_locations(locations, fileName, path="./"):
    _base_input_check(locations)
    import folium
    from folium.plugins import HeatMap
    from .infrastructure import SuperMap
    map_keys = locations["省"] + "," + locations["市"] + "," + locations["区"]
    heatData = []
    for map_key in map_keys:
        if SuperMap.lat_lon_mapper.get(map_key):
            lat_lon = SuperMap.lat_lon_mapper[map_key]
            heatData.append([lat_lon[0], lat_lon[1], 1])
    map_osm = folium.Map(location=[35,110],zoom_start=5)    #绘制Map，开始缩放程度是5倍
    HeatMap(heatData).add_to(map_osm)  # 将热力图添加到前面建立的map里
    file_path = path + fileName
    map_osm.save(file_path) #保存为html文件
    
    
def echarts_draw(locations, fileName, path="./", title="地域分布图"
                 , subtitle="location distribute"):
    
    """
    生成地域分布的echarts热力图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param fileName: 生成的html文件的文件名.
    :param path: 生成的html文件的路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    """
    from pyecharts import Geo
    
    _base_input_check(locations)
    map_keys = locations["省"] + "," + locations["市"] + "," + locations["区"]
    count_map = {}
    from .infrastructure import SuperMap
    for map_key in map_keys:
        if SuperMap.lat_lon_mapper.get(map_key):
            count_map[map_key] = count_map.get(map_key, 0) + 1
    
    geo = Geo(title, subtitle, title_color="#fff",
          title_pos="center", width=1200,
          height=600, background_color='#404a59')
    _geo_update(geo)
    attr, value = geo.cast(count_map)
    geo.add("", attr, value, type="heatmap", is_visualmap=True,
        visual_text_color='#fff',
        is_piecewise=True, visual_split_number=10)
    geo.render(path + fileName)
    
def echarts_cate_draw(locations, labels, fileName, path="./"
                      , title="地域分布图", subtitle="location distribute",
                      point_size=7):
    """
    依据分类生成地域分布的echarts散点图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param labels: 长度必须和locations相等, 代表每个样本所属的分类.
    :param fileName: 生成的html文件的文件名.
    :param path: 生成的html文件的路径.
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
    
    from .infrastructure import SuperMap
    def _data_add(_geo, _cate_keys, _category):
        real_keys = []
        for cate_key in _cate_keys:
            if SuperMap.lat_lon_mapper.get(cate_key):
                real_keys.append(cate_key)
        
        attr = real_keys
        value = [1] * len(real_keys)
        geo.add(_category, attr, value, symbol_size=point_size,
                legend_pos="left", legend_top="bottom", 
                geo_normal_color="#fff",
                geo_emphasis_color =" #f0f0f5")
    
    for category in uniques:
        cate_locations = locations[labels == category]
        _data_add(geo, cate_locations["省"] + "," + cate_locations["市"] + \
                  "," + cate_locations["区"], category)
        
    geo.render(path + fileName)
        
        
    
    
    
    
    
    
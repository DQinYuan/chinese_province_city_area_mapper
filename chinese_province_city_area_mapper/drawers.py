# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 13:38:00 2018

@author: 燃烧杯
"""


def draw_locations(locations, fileName, path="./"):
    import pandas as pd
    if not isinstance(locations, pd.DataFrame):
        from .exceptions import InputTypeNotSuportException
        raise InputTypeNotSuportException(InputTypeNotSuportException.input_type)
    if "省" not in locations.columns or "市" not in locations.columns \
         or "区" not in locations.columns:
        raise InputTypeNotSuportException(InputTypeNotSuportException.input_type)
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
    
    
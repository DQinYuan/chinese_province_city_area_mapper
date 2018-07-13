# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 00:47:32 2018

@author: 燃烧杯
"""

from .infrastructure import Record

class CPCATransformer:
    
    #可以传入用户自定义区县map，因为原始数据区县map有很多key重复
    def __init__(self, u_map={}):
        self.umap = u_map
    
    def transform(self, data):
        from .infrastructure import SuperMap
        SuperMap.rep_area_set = set()
        import pandas as pd
        if isinstance(data, pd.Series):
            data = data.astype(str)
        lines = []
        for line in data:
            lines.append(Record(line).pca_map(self.umap))
        
        import logging
        if len(SuperMap.rep_area_set) != 0:
            logging.warning("建议添加到umap中的区有：" + str(SuperMap.rep_area_set)
             + ",有多个市含有相同名称的区")
        
        import pandas as pd
        return pd.concat(lines, ignore_index=True)
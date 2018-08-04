# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 00:55:14 2018

@author: 燃烧杯
"""

import jieba

class Record:
    def __init__(self, line):
        from .domain import Location
        self.location = Location()
        self.address = ""
        #默认选取第一个遇到的省，市或者自治区
        for word in jieba.cut(line):
            #因为jieba对"上海浦东区"的分词会出现问题，所以这里单独处理
            if word == "上海市浦东新区":
                self.location.setPlace("上海市", SuperMap.CITY)
                self.location.setPlace("浦东新区", SuperMap.AREA)
                continue
            
            word_type = SuperMap.getType(word)
            
            if word_type:
                self.location.setPlace(word, word_type)
            else:
                self.address += word
            
        self.location.setPlace(self.address, SuperMap.ADDRESS)
        
    def pca_map(self, umap):
         return self.location.pca_map(umap)
            
    
        

            

class SuperMap:
    from .mappers import area_city_mapper, city_province_mapper,\
                        province_country_mapper, rep_areas, \
                        lat_lon_mapper
    
    AREA = "area"
    CITY = "city"
    PROVINCE = "province"
    ADDRESS = "address"
    
    rep_area_set = set()
    
    @classmethod
    def getType(cls, word):
        if cls.area_city_mapper.get(word):
            return cls.AREA
        if cls.city_province_mapper.get(word):
            return cls.CITY
        if cls.province_country_mapper.get(word):
            return cls.PROVINCE
        return ""
    
    #如果将“北京市”简写作“北京”，则补全“市”字
    @classmethod
    def fillCity(cls, word):
        if word and not word.endswith("市") \
                and not word.endswith("盟") \
                and not word.endswith("地区") \
                and not word.endswith("自治州"):
            return word + "市", True
        return word, False
        
    #如果将“重庆省”简写成“重庆”，则补全“省字”
    @classmethod
    def fillProvince(cls, word):
        if word and not word.endswith("市") and not word.endswith("省"):
            if cls.province_country_mapper.get(word + "市"):
                return word + "市", True
            if cls.province_country_mapper.get(word + "省"):
                return word + "省", True
        return word, False
            
    
        
    
        
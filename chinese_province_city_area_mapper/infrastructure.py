# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 00:55:14 2018

@author: 燃烧杯
"""

import jieba

class Record:
    def __init__(self, line, cut=True, lookahead=8):
        from .domain import Location
        self.location = Location()
        self.address = ""
        if cut:#分词模式
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
        else:   #完整匹配模式
            i = 0
            while i < len(line):
                sub = line[i:]
                word,word_type = SuperMap.getStartsType(sub, lookahead)
                if word_type:
                    i += len(word)
                    self.location.setPlace(word, word_type)
                    continue
                self.address += line[i]
                i += 1
                    
                    
            
        self.location.setPlace(self.address, SuperMap.ADDRESS)
        
    def pca_map(self, umap):
         return self.location.pca_map(umap)
            
    
        

            
'''
负责管理省市区映射信息
'''
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
    
    @classmethod
    def getStartsType(cls, sub, lookahead=8):
        # 如果sub字符串的长度超过8，则也只看前八位
        bound = lookahead if len(sub) > lookahead else len(sub)
        #总是返回匹配到的最长字符串，所以从后往前遍历
        for i in range(bound, 0, -1):
            subsub = sub[:i]
            subtype = cls.getType(subsub)
            if subtype:
                return subsub, subtype
        return "",""
            
            
            
    
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
        #以下区域需要采用特殊的填充策略
        if word and word == '新疆':
            return '新疆维吾尔族自治区',True
        if word and word == '宁夏':
            return '宁夏回族自治区',True
        if word and word == '西藏':
            return '西藏自治区',True
        if word and word == '广西':
            return '广西壮族自治区',True
        return word, False
            
    
        
    
        
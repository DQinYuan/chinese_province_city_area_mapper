# -*- coding: utf-8 -*-

from collections import defaultdict

P = 0
C = 1
A = 2


class AddrMap(defaultdict):
    """封装 '地名' -> [[相关地址列表], 地名全名]   这种映射结构"""

    def __init__(self):
        super().__init__(lambda: [[], None])

    def get_full_name(self, key):
        return self[key][1]

    def is_unique_value(self, key):
        """key所映射到的地址列表中的地址是否唯一"""
        if key not in self.keys():
            return False
        
        return len(self.get_relational_addrs(key)) == 1

    def get_relational_addrs(self, key):
        return self[key][0]

    def get_value(self, key, pos):
        """获得映射的第一个地址, 必须保证该key存在, 不然会出错"""
        return self.get_relational_addrs(key)[0][pos]

    def append_relational_addr(self, key, pca_tuple, full_name_pos):
        self[key][0].append(pca_tuple)
        if not self[key][1]:
            self[key][1] = pca_tuple[full_name_pos]


class Pca(object):

    def __init__(self, province = '', city = '', area = '', province_pos = -1, city_pos = -1, area_pos = -1):
        self.province = province
        self.city = city
        self.area = area
        self.province_pos = province_pos
        self.city_pos = city_pos
        self.area_pos = area_pos

    def propertys_dict(self, pos_sensitive):
        result = {
            "省": self.province,
            "市": self.city,
            "区": self.area
        }

        if pos_sensitive:
            result["省_pos"] = self.province_pos
            result["市_pos"] = self.city_pos
            result["区_pos"] = self.area_pos

        return result
# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""


if __name__ == '__main__':
    ## 查询经纬度信息
    from address_extractor import latlng

    a = latlng[('北京市', '北京市', '朝阳区')]  # 输出('39.95895316640668', '116.52169489108084')
    print(a)
    ## 查询含有"鼓楼区"的全部地址
    from address_extractor import area_map

    print(area_map.get_relational_addrs('鼓楼区'))  # [('江苏省', '南京市', '鼓楼区'), ('江苏省', '徐州市', '鼓楼区'), ('福建省', '福州市', '鼓楼区'), ('河南省', '开封市', '鼓楼区')]
    #### 注: city_map可以用来查询含有某个市的全部地址, province_map可以用来查询含有某个省的全部地址

    ## 查询含有"江苏省", "鼓楼区"的全部地址
    from address_extractor import province_area_map

    print(province_area_map.get_relational_addrs(('江苏省', '鼓楼区')))  # [('江苏省', '南京市', '鼓楼区'), ('江苏省', '徐州市', '鼓楼区')]


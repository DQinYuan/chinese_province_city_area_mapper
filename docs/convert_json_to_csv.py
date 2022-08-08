# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import json

input_file = 'hk_mo_tw.json'
output_file = 'hk_mo_tw.csv'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# {"北京市":{"市辖区":["东城区","西城区","朝阳区"]}, "": {}}
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('country,province,city,area,lat,lng\n')
    for k, v in data.items():
        # k = 北京市
        for kk, vv in v.items():
            # kk=市辖区
            new_kk = k if kk == '市辖区' else kk
            for m in vv:
                f.write(f'中国,{k},{new_kk},{m},,\n')

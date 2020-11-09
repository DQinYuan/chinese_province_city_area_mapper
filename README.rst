chinese_province_city_area_mapper
==================================

chinese_province_city_area_mapper：一个用于识别简体中文字符串中省，市和区并能够进行映射，检验和简单绘图的python模块

举个例子::

    ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            ↓ 转换
   |省    |市   |区    |地址                 |
   |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
   |福建省|泉州市|洛江区|万安塘西工业区        |

chinese_province_city_area_mapper: built to be recognize Chinese province,city and area in simplified Chinese string, it can automaticall map area to city
and map city to province.

for example::

    ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            ↓ transform
   |省    |市   |区    |地址                 |
   |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
   |福建省|泉州市|洛江区|万安塘西工业区        |

完整文档见该模块的Github，
GitHub: `https://github.com/DQinYuan/chinese_province_city_area_mapper <https://github.com/DQinYuan/chinese_province_city_area_mapper>`_


安装说明
========
代码目前仅仅支持python3
    pip install cpca

Get Started
============

本模块中最主要的方法是cpca.transform,
该方法可以输入任意的可迭代类型（如list，pandas的Series类型等），
然后将其转换为一个DataFrame，下面演示一个最为简单的使用方法::

    location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "北京朝阳区北苑华贸城"]
    import cpca
    df = cpca.transform(location_str)
    df

输出的结果为::

       省     市    区          地址              adcode
    0 上海市 上海市  徐汇区     虹漕路461号58号楼5楼  310104
    1 福建省 泉州市  洛江区     万安塘西工业区        350504
    2 北京市 市辖区  朝阳区     北苑华贸城           110105

如果还想知道更多的细节，请访问该
模块的github地址 `https://github.com/DQinYuan/chinese_province_city_area_mapper <https://github.com/DQinYuan/chinese_province_city_area_mapper>`_，
在那里我写了更多的细节
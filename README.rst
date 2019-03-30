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

    location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
    import cpca
    df = cpca.transform(location_str)
    df

输出的结果为::

         省    市      区         地址
    0  上海市  上海市  徐汇区   虹漕路461号58号楼5楼
    1  福建省  泉州市  洛江区   万安塘西工业区
    2  北京市  北京市  朝阳区   北苑华贸城

**全文模式**：

jieba分词并不能百分之百保证分词的正确性，在分词错误的情况下会造成奇怪的结果，比如下面::

    location_str = ["浙江省杭州市下城区青云街40号3楼"]
    import cpca
    df = cpca.transform(location_str)
    df

输出的结果为::

    省      市     区    地址
    浙江省  杭州市 城区   下青云街40号3楼

这种诡异的结果因为jieba本身就将词给分错了，所以我们引入了全文模式，不进行分词，直接全文匹配，使用方法如下::

    location_str = ["浙江省杭州市下城区青云街40号3楼"]
    import cpca
    df = cpca.transform(location_str, cut=False)
    df

输出结果::

     省    市      区        地址
   浙江省  杭州市   下城区    青云街40号3楼

这些就完全正确了，不过全文匹配模式会造成效率低下，我默认会向前看8个字符(对应transform中的lookahead参数默认值为8)，这个是比较保守的，因为有的地名会比较长（比如“新疆维吾尔族自治区”），如果你的地址库中都是些短小的省市区名的话，可以选择将lookahead设置得小一点，比如::

    location_str = ["浙江省杭州市下城区青云街40号3楼"]
    import cpca
    df = cpca.transform(location_str, cut=False, lookahead=3)
    df

输出结果与上面一样。

如果还想知道更多的细节，请访问该
模块的github地址 `https://github.com/DQinYuan/chinese_province_city_area_mapper <https://github.com/DQinYuan/chinese_province_city_area_mapper>`_，
在那里我写了更多的细节
# -*- coding: utf-8 -*-
from setuptools import setup

LONGDOC = """

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

特点
====

-  基于jieba分词进行匹配，同时加入了一些额外的校验匹配逻辑保证了准确率

-  因为jieba分词本身只有80%的准确率，经常会分错，所以引入了全文匹配的模式，这种模式下能够提高准确率，但会导致性能降低，关于如何开启这个模式见Github上的使用文档

-  如果地址数据比较脏的，不能指望依靠这个模块达到100%的准确，本模块只能保证尽可能地提取信息，如果想要达到100%准确率的话，最好在匹配完后再人工核验一下

-  自带完整的省，市，区三级地名及其经纬度的数据

-  支持自定义省，市，区映射

-  输出的是基于pandas的DataFrame类型的表结构，易于理解和使用

-  封装了简单的绘图功能，可以很方便地进行简单的数据可视化

-  MIT 授权协议

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
    from cpca import *
    df = transform(location_str)
    df


输出的结果为::

         区    市      省         地址
    0  徐汇区  上海市  上海市   虹漕路461号58号楼5楼
    1  洛江区  泉州市  福建省   万安塘西工业区
    2  朝阳区  北京市  北京市   北苑华贸城

**全文模式**：

jieba分词并不能百分之百保证分词的正确性，在分词错误的情况下会造成奇怪的结果，比如下面::

    location_str = ["浙江省杭州市下城区青云街40号3楼","广东省东莞市莞城区东莞大道海雅百货"]
    from cpca import *
    df = transform(location_str)
    df

输出的结果为::

    区    市    省            地址
    城区  东莞市  广东省  莞大道海雅百货自然堂专柜
    城区  杭州市  浙江省  下青云街40号3楼

这种诡异的结果因为jieba本身就将词给分错了，所以我们引入了全文模式，不进行分词，直接全文匹配，使用方法如下::

    location_str = ["浙江省杭州市下城区青云街40号3楼","广东省东莞市莞城区东莞大道海雅百货"]
    from cpca import *
    df = transform(location_str, cut=False)
    df

输出结果::

     区    市    省        地址
   下城区  杭州市  浙江省  青云街40号3楼
   莞城区  东莞市  广东省    大道海雅百货

这些就完全正确了，不过全文匹配模式会造成效率低下，我默认会向前看8个字符(对应transform中的lookahead参数默认值为8)，这个是比较保守的，因为有的地名会比较长（比如“新疆维吾尔族自治区”），如果你的地址库中都是些短小的省市区名的话，可以选择将lookahead设置得小一点，比如::

    location_str = ["浙江省杭州市下城区青云街40号3楼","广东省东莞市莞城区东莞大道海雅百货"]
    from cpca import *
    df = transform(location_str, cut=False, lookahead=3)
    df

输出结果与上面一样。


如果还想知道更多的细节，请访问该
模块的github地址 `https://github.com/DQinYuan/chinese_province_city_area_mapper <https://github.com/DQinYuan/chinese_province_city_area_mapper>`_，
在那里我写了更多的细节.

"""

requires = ['pandas(>=0.20.0)',
           'jieba(>=0.39)',
           ]  


setup(name='cpca',
      version='0.3.5',
      description='Chinese Province, City and Area Recognition Utilities',
      long_description=LONGDOC,
      author='DQinYuan',
      author_email='sa517067@mail.ustc.edu.cn',
      url='https://github.com/DQinYuan/chinese_province_city_area_mapper',
      license="MIT",
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
      ],
      keywords='Simplified Chinese,Chinese geographic information,Chinese province city and area recognition and map',
      packages=['chinese_province_city_area_mapper', ''],
      package_dir={'chinese_province_city_area_mapper':'chinese_province_city_area_mapper',
                   '':'.',},    #必须写成'.',而不能写成'./'
      install_requires = requires, 
)
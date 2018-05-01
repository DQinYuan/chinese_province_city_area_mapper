# -*- coding: utf-8 -*-
from distutils.core import setup

LONGDOC = """

chinese_province_city_area_mapper
==================================

chinese_province_city_area_mapper：一个用于识别简体中文字符串中省，市和区并能够进行映射，检验和简单绘图的python模块

举个例子::
                                                            
    ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            ↓ 转换
    |省    |市   |区    |
    |上海市|上海市|徐汇区|
    |福建省|泉州市|洛江区|


chinese_province_city_area_mapper: built to be recognize Chinese province,city and area in simplified Chinese string, it can automaticall map area to city 
and map city to province.
for example::

    ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            ↓ transform
    |省    |市   |区    |
    |上海市|上海市|徐汇区|
    |福建省|泉州市|洛江区|


 
完整文档见该模块的Github，
GitHub: `https://github.com/DQinYuan/chinese_province_city_area_mapper <https://github.com/DQinYuan/chinese_province_city_area_mapper>`_

特点
====

-  基于jieba分词进行匹配，同时拥有比较复杂的匹配逻辑保证了准确率，笔者根据手头的海量地址描述数据进行了测试

-  自带完整的省，市，区三级地名及其经纬度的数据

-  支持自定义省，市，区映射

-  输出的是基于pandas的DataFrame类型的表结构，易于理解和使用

-  封装了简单的绘图功能，可以很方便地进行简单的数据可视化

-  MIT 授权协议

安装说明
========

代码目前仅仅支持python3

    pip install chinese_province_city_area_mapper

Get Started
============

本模块中最主要的类是chinese_province_city_area_mapper.transformer.CPCATransformer（注：CPCA是Chinese Province City Area的缩写），
该类的transform方法可以输入任意的可迭代类型（如list，Series等），然后将其转换为一个DataFrame，
示例代码如下::

    location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
    from chinese_province_city_area_mapper.transformer import CPCATransformer
    cpca = CPCATransformer()
    df = cpca.transform(location_str)
    df


输出的结果为::

         区    市    省
    0  徐汇区  上海市  上海市
    1  洛江区  泉州市  福建省
    2  朝阳区 

从上面的程序输出中你会发现朝阳区并没有被映射到北京市，这是因为在中国有多个同名的叫做朝阳区的区，
并且他们位于不同的市，所以程序就不知道该映射到哪一个市了，因此就不对其进行映射，如果你确定你
的数据中的朝阳区都是指北京市的那个朝阳区的话，可以在CPCATransformer的构造函数中传一个字典
（叫做umap参数，是user map的简称），指定朝阳区都要映射到北京市，
注意只有区到市的这一级映射存在重名问题，中国的市的名称都是唯一的，省的名称也都是唯一的
，示例代码如下::

    location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
    from chinese_province_city_area_mapper.transformer import CPCATransformer
    cpca = CPCATransformer({"朝阳区":"北京市"})
    df = cpca.transform(location_str)
    df


输出结果为::
    
         区    市    省
    0  徐汇区  上海市  上海市
    1  洛江区  泉州市  福建省
    2  朝阳区  北京市  北京市

模块中还内置了一个我推荐大家使用的umap，这个umap中我根据处理地址数据的经验将那些重名的区映射到了它最常见的一个市，
这个umap位于chinese_province_city_area_mapper.myumap.umap，使用如下::

    location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
    from chinese_province_city_area_mapper.transformer import CPCATransformer
    from chinese_province_city_area_mapper import myumap
    print(myumap.umap)   #查看这个umap的内容
    cpca = CPCATransformer(myumap.umap)
    df = cpca.transform(location_str)
    df

输出和上一个程序一样


模块中还自带一个简单绘图工具，可以在地图上将上面输出的数据以热力图的形式画出来
，代码如下::

    from chinese_province_city_area_mapper import drawers
    #df为上一段代码输出的df
    drawers.draw_locations(df, "df.html")


这一段代码运行结束后会在运行代码的当前目录下生成一个df.html文件，用浏览器打开即可看到
绘制好的地图（如果某条数据'省'，'市'或'区'字段有缺，则会忽略该条数据不进行绘制）。

draw_locations函数还可以通过指定path参数来改变输出路径，示例代码如下::

    from chinese_province_city_area_mapper import drawers
    #在当前目录的父目录生成df.html
    drawers.draw_locations(df, "df.html", path="../")

本模块的基本使用方法大概就是这些了，如果还想知道更多的细节，请访问该
模块的github地址 `https://github.com/DQinYuan/chinese_province_city_area_mapper <https://github.com/DQinYuan/chinese_province_city_area_mapper>`_，
在那里我写了更多的细节，2.0及以上版本又增加了几个echarts的绘图方便函数，见Github。

"""

requires = ['pandas(>=0.20.0)',
           'folium(>=0.5.0)',
           'jieba(>=0.39)',
           'pyecharts(>=0.5.0)',
           'echarts-countries-pypkg(>=0.1.4)',
           'pyecharts-snapshot(>=0.1.5)',
           ]  


setup(name='chinese_province_city_area_mapper',
      version='2.2',
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
      packages=['chinese_province_city_area_mapper'],
      package_dir={'chinese_province_city_area_mapper':'chinese_province_city_area_mapper'},
      package_data={'chinese_province_city_area_mapper':['*.*']},
      install_requires = requires, 
)
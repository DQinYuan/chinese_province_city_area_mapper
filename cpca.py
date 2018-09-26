# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 22:50:55 2018

@author: 燃烧杯
"""

myumap = {'南关区': '长春市',
 '南山区': '深圳市',
 '宝山区': '上海市',
 '市辖区': '东莞市',
 '普陀区': '上海市',
 '朝阳区': '北京市',
 '河东区': '天津市',
 '白云区': '广州市',
 '西湖区': '杭州市',
 '铁西区': '沈阳市'}

def transform(location_strs, umap=myumap, index=[], cut=True, lookahead=8):
    """将地址描述字符串转换以"省","市","区"信息为列的DataFrame表格
        Args:
            locations:地址描述字符集合,可以是list, Series等任意可以进行for in循环的集合
                      比如:["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            umap:自定义的区级到市级的映射,主要用于解决区重名问题,如果定义的映射在模块中已经存在，则会覆盖模块中自带的映射
            index:可以通过这个参数指定输出的DataFrame的index,默认情况下是range(len(data))
            cut:是否使用分词，默认使用，分词模式速度较快，但是准确率可能会有所下降
            lookahead:只有在cut为false的时候有效，表示最多允许向前看的字符的数量
                      默认值为8是为了能够发现"新疆维吾尔族自治区"这样的长地名
                      如果你的样本中都是短地名的话，可以考虑把这个数字调小一点以提高性能
        Returns:
            一个Pandas的DataFrame类型的表格，如下：
               |省    |市   |区    |地址                 |
               |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
               |福建省|泉州市|洛江区|万安塘西工业区        |
            
    """
    from chinese_province_city_area_mapper.transformer import CPCATransformer
    cpca = CPCATransformer(umap)
    # loc这里的作用纯粹是为了让输出结果更好看一些
    return cpca.transform(location_strs, index, cut, lookahead).loc[:, ('区','市','省','地址')]



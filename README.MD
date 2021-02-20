
[![Build Status](https://www.travis-ci.org/DQinYuan/chinese_province_city_area_mapper.svg?branch=master)](https://www.travis-ci.org/DQinYuan/chinese_province_city_area_mapper)
# 简介

一个用于提取简体中文字符串中省，市和区并能够进行映射，检验和简单绘图的python模块。

举个例子：

    ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            ↓ 转换
    |省    |市   |区    |地址                 |
    |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
    |福建省|泉州市|洛江区|万安塘西工业区        |

> 注：“地址”列代表去除了省市区之后的具体地址

也可以将大段文本中所有提到的地址提取出来，并且自动将相邻的存在所属关系的地址归并到一条记录中（0.5.5版本新功能）：

    "分店位于徐汇区虹漕路461号58号楼5楼和泉州市洛江区万安塘西工业区以及南京鼓楼区"
            ↓ 转换
    |省    |市   |区    |
    |上海市|上海市|徐汇区|
    |福建省|泉州市|洛江区|
    |江苏省|南京市|鼓楼区|

# 安装说明

代码目前仅仅支持python3

`pip install cpca`

> 注:cpca是chinese province city area的缩写

如果觉得本模块对你有用的话，施舍个star，谢谢。

常见安装问题：

在 windows 上可能会出现类似如下问题

```
Building wheel for pyahocorasick (setup.py) ... error
```

先去下载  [Microsoft Visual C++ Build Tools](https://link.zhihu.com/?target=http%3A//go.microsoft.com/fwlink/%3FLinkId%3D691126)，
安装完成后，再重新使用 pip install cpca 安装，即可解决问题

# 中国行政区划分数据获取

提取自 @Vonng 维护的项目 [adcode](https://github.com/Vonng/adcode)，里面包含中国的所有行政区划和编码

提取的数据文件在为[cpca/resources/adcodes.csv](./cpca/resources/adcodes.csv)

笔者会定期从 adcode 中同步，如果同步的不及时，可以使用本仓库中的 [local-sync.py](local-sync.py) 脚本进行同步，使用方法如下：

```shell
git clone git@github.com:Vonng/adcode.git
python local-sync.py <adcode所在目录>
```

# Get Started


本模块中最主要的方法是`cpca.transform`，该方法可以输入任意的可迭代类型（如list，pandas的Series类型等），然后将其转换为一个DataFrame，下面演示一个最为简单的使用方法：

```python
location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "北京朝阳区北苑华贸城"]
import cpca
df = cpca.transform(location_str)
df
```


输出的结果为(adcode为官方地址编码)：

       省     市    区          地址              adcode
    0 上海市 上海市  徐汇区     虹漕路461号58号楼5楼  310104
    1 福建省 泉州市  洛江区     万安塘西工业区        350504
    2 北京市 市辖区  朝阳区     北苑华贸城           110105

> 注：程序输出的df是一个Pandas的DataFrame类型变量，DataFrame可以非常轻易地转化为csv或者excel文件，如果你对DataFrame不熟悉的话，可以参考Pandas的官方文档：http://pandas.pydata.org/pandas-docs/version/0.20/dsintro.html#dataframe
>
> ，或者往下翻到"示例与测试用例"大标题，那里我也展示了DataFrame的拼接与转换成csv文件的操作。


> 地理小提示：在中国行政区划中，直辖市的区都不是直接挂在直辖市下面的，而是挂在唯一的一个市辖区下面，普通的市下面也会有市辖区，但是普通的市辖区只是
> 三级行政单位，不像直辖市的市辖区，是二级行政单位

如果你想获知程序是从字符串的那个位置提取出省市区名的，可以添加一个`pos_sensitive=True`参数：

```python
location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "北京朝阳区北苑华贸城"]
import cpca
df = cpca.transform(location_str, pos_sensitive=True)
df
```

输出如下：

```
     省    市    区        地址               adcode        省_pos  市_pos 区_pos
0  上海市  上海市  徐汇区  虹漕路461号58号楼5楼   310104     -1     -1      0
1  福建省  泉州市  洛江区  万安塘西工业区         350504     -1      0      3
2  北京市  市辖区  朝阳区  北苑华贸城            110105     -1     -1      0
```

其中`省_pos`，`市_pos`和`区_pos`三列大于-1的部分就代表提取的位置。-1则表明这个字段是靠程序推断出来的，或者没能提取出来。


有的时候为了方便`concat`，想要自定义输出表的index，可以选择使用transform函数的index参数(这个参数只要保证长度和data相同即可，可以是list或者pandas中相关的类型)，示例如下：

```python
location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "北京朝阳区北苑华贸城"]
import cpca
df = cpca.transform(location_str, index=["2018年","2017年","2016年"])
df
```

输出结果：

```
        省      市      区      地址              adcode
2018年  上海市  上海市  徐汇区  虹漕路461号58号楼5楼  310104
2017年  福建省  泉州市  洛江区  万安塘西工业区        350504
2016年  北京市  市辖区  朝阳区  北苑华贸城           220104
```

中国的区级行政单位非常的多，经常有重名的情况，比如“北京市朝阳区”和“吉林省长春市朝阳区”，当有上级地址信息的时候，cpca 能够根据上级地址
推断出这是哪个区，但是如果没有上级地址信息，单纯只有一个区名的时候， cpca 就没法推断了，只能随便选一个了，
通过 umap 参数你可以指定这种情况下该选择哪一个：

```python
import cpca
cpca.transform(["朝阳区汉庭酒店大山子店"])
#     省    市    区        地址  adcode
#0  吉林省  长春市  朝阳区  汉庭酒店大山子店  220104
cpca.transform(["朝阳区汉庭酒店大山子店"],umap={"朝阳区":"110105"})
#     省    市    区        地址  adcode
#0  北京市  市辖区  朝阳区  汉庭酒店大山子店  110105
```

从例子可以看出，umap 字典的 key 是区名，value 是区的 adcode，这里 `110105` 就是北京市朝阳区的 adcode，具体的 adcode 可以去
[全国行政区划查询平台](http://xzqh.mca.gov.cn/map) 上查询。

从大段文本中提取多个地址（0.5.5版本新功能）：

```python
import cpca
df = cpca.transform_text_with_addrs("分店位于徐汇区虹漕路461号58号楼5楼和泉州市洛江区万安塘西工业区以及南京鼓楼区")
df
```

结果为（注意 transform_text_with_addrs 获得的数据，“地址”列都是空的）：

```
    省     市     区    地址   adcode
0  上海市  市辖区  徐汇区       310104
1  福建省  泉州市  洛江区       350504
2  江苏省  南京市  鼓楼区       320106
```

`transform_text_with_addrs` 还支持和 `transform` 类似的 `index`, `pos_sensitive` 以及 `umap` 参数

**绘图：**

模块中还自带一些简单绘图工具，可以在地图上将上面输出的数据以热力图的形式画出来.

这个工具依赖folium，为了减小本模块的体积，所以并不会预装这个依赖，在使用之前请使用`pip install folium ` .

代码如下：

```python
from cpca import drawer
#df为上一段代码输出的df
drawer.draw_locations(df[cpca._ADCODE], "df.html")
```

这一段代码运行结束后会在运行代码的当前目录下生成一个df.html文件，用浏览器打开即可看到
绘制好的地图（如果某条数据'省'，'市'或'区'字段有缺，则会忽略该条数据不进行绘制），速度会比较慢，需要耐心等待，绘制的图像如下：

![绘图展示](https://user-images.githubusercontent.com/23725000/39467918-143b576e-4d63-11e8-9325-8c68651ffcc2.png)


还有更多的绘图工具请参考文档的大标题为“示例与测试用例”的部分。

到这里就你就已经知道了本模块的基本使用了，接下来我会阐明更多细节。

# 关于匹配与映射的细节

为了保证匹配与映射的正确性，我做了很多细节上的处理，如果在使用本模块的过程中遇到困惑可以参考这里。

 - 能够匹配到省或者市的缩写，比如将"北京市"缩写为"北京"，"江苏省"缩写为"江苏"，依旧能够匹配到并且能够自动补全为全称，示例代码如下：

```python
#测试数据
location_strs = ["江苏省南京市鼓楼区256号", "江苏南京鼓楼区256号"]

import cpca
df = cpca.transform(location_strs)
df
```

输出的结果为：

```
     区    市     省       地址   adcode
0  鼓楼区  南京市  江苏省   256号   320106
1  鼓楼区  南京市  江苏省   256号   320106
```

我不仅做了这些缩写情况处理，还处理了诸如"新疆维吾尔族自治区"缩写为"新疆"，"西藏藏族自治区"缩写为"西藏"等情况，如下：

```python
import cpca

location_str = ["新疆","广西","宁夏","西藏"]
df = cpca.transform(location_str)
df
```

输出：

```
   省                 市    区   地址   adcode
0  新疆维吾尔自治区                      650000
1  广西壮族自治区                        450000
2  宁夏回族自治区                        640000
3  西藏自治区                           540000
```


 - 以先出现的地名为准
 
 ```python
#测试数据
location_strs = ["江苏省南京市徐州市鼓楼区256号"]

import cpca
df = cpca.transform(location_strs)
df
```

后出现的徐州市并没有被提取。

 - 最后一列的地址字段，本质上是截取最后一个地名后面的文字
 
 
 ```python
import cpca
cpca.transform(["11月15日早上9点到11月18日下班前王大猫。在观山湖区"], pos_sensitive=True)
 ```
输出为:

```
    省     市      区        地址   adcode      省_pos 市_pos 区_pos
0  贵州省  贵阳市  观山湖区           520115     -1     -1     25
```

"观山湖区" 后面已经没有文字可以截取了，所以 “地址” 部分就是一个空字符串

# 示例与测试用例

本仓库放了一份大约一万多条地址描述信息[tests/addr.csv](https://github.com/DQinYuan/chinese_province_city_area_mapper/blob/master/tests/addr.csv)
，用于测试模块，测试代码如下：



*测试基本功能：*

```python
#读取数据
import pandas as pd
origin = pd.read_csv("tests/addr.csv")
#转换
import cpca
addr_df = cpca.transform(origin["原始地址"])
#输出
processed = pd.concat([origin, addr_df], axis=1)
processed.to_csv("processed.csv", index=False, encoding="utf-8")
```

注意以上代码运行结束后会打印一句warnning，这些warnning是因为程序无法确定某个区县属于哪个市（因为这些区县存在重名问题而且在umap中又没有指定它属于哪一个市）.

*测试绘图函数1（绘制热力图）：*

 模块中绘制热力图的函数是基于folium编写的，为了减小模块体积，在安装模块时没有安装这些绘图库的依赖，如果需要使用这个函数的话，需要先使用`pip install folium  `安装folium  

```python
from cpca import drawer
#processed为上一段代码的processed
drawer.draw_locations(processed[cpca._ADCODE], "processed.html")
```

用浏览器打开"processed.html"文件，发现绘制的局部图像如下（在国内folium的地图显示速度比较慢，所以需要耐心等待地图显示）：

![长三角热力图](https://user-images.githubusercontent.com/23725000/39467928-1e7190ae-4d63-11e8-93c4-39f2b2e5432c.png)

（注意：本模块在绘图时，只绘制那些可以精确地匹配到省市区的地址，对于省市区有一个或多个字段缺失的则会直接忽略）

*测试绘图函数2（绘制echarts热力图）:*

因为在国内folium的地图显示速度太慢了，所以添加了echarts的热力图绘图函数.

在使用本函数之前需要先用如下命令安装它的依赖（为了减少本模块的体积，所以这些依赖不会被自动安装）：

```
pip install pyecharts==0.5.11
pip install echarts-countries-pypkg
pip install pyecharts-snapshot
```

示例代码如下，仍然使用之前的测试数据生成的processed变量：
```python
from cpca import drawer
drawer.echarts_draw(processed[cpca._ADCODE], "echarts.html")
```

该接口的更多参数及其含义如下：
```python
def echarts_draw(locations, file_path, title="地域分布图"
                 , subtitle="location distribute"):
    """
    生成地域分布的echarts热力图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param file_path: 生成的html文件路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    """
```

然后会在当前目录下生成一个echarts.html文件，用浏览器打开后即可看到图像：

![echarts热力图](https://user-images.githubusercontent.com/23725000/39467908-0d60e3a0-4d63-11e8-8f25-06df97dd2889.png)

*测试绘图函数3(绘制分类信息图)：*

在使用本函数之前需要安装的依赖同上一个绘图函数，如果你是跳过了前面的直接读到这里的话，务必向上翻看一下。

样本分类绘制函数，通过额外传入一个样本的分类信息，能够在地图上以不同的颜色画出属于不同分类的样本散点图，以下代码以“省”作为类别信息绘制分类散点图（可以看到，属于不同省的样本被以不同的颜色标记了出来，这里以“省”作为分类标准只是举个例子，实际应用中可以选取更加有实际意义的分类指标）：

```python
from cpca import drawer
drawer.echarts_cate_draw(processed[cpca._ADCODE], processed["省"], "echarts_cate.html")
```

然后会在当前目录下生成一个echarts_cate.html文件，用浏览器打开后即可看到图像：

![echarts分类散点图](https://user-images.githubusercontent.com/23725000/39467901-0471419a-4d63-11e8-92fd-63bab219a766.png)

该接口更多的参数及其含义如下：

```python
def echarts_cate_draw(locations, labels, file_path, title="地域分布图", subtitle="location distribute",
                      point_size=7):
    """
    依据分类生成地域分布的echarts散点图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param labels: 长度必须和locations相等, 代表每个样本所属的分类.
    :param file_path: 生成的html文件路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    :param point_size: 每个散点的大小
    """
```

# How to Contribute

项目代码还很粗糙，如果大家对代码有所改进，欢迎提交回本项目
，在提交之前，注意以下两点：

 - 在`tests`添加相应的单元测试
 - 使用`python setup.py test`来运行所有单元测试，确保所有单测都是通过的
 
之后即可提交PR

# END

如果大家在使用过程中发现一些匹配错误的地址，欢迎提issue来帮助我收集这些错误用例和改善算法，毕竟笔者手头数据有限，难以考虑到所有边界情况
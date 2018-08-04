# 简介

一个用于提取简体中文字符串中省，市和区并能够进行映射，检验和简单绘图的python模块。

举个例子：

    ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            ↓ 转换
    |省    |市   |区    |地址                 |
    |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
    |福建省|泉州市|洛江区|万安塘西工业区        |

> 注：“地址”列代表去除了省市区之后的具体地址

# 安装说明

代码目前仅仅支持python3

`pip install cpca`

> 注:cpca是chinese province city area的缩写



常见安装错误：

​     有的朋友在我的博客中反映他们在使用的时候会报如下错误：

```
ModuleNotFoundError: No module named 'jieba'
```

​            可能是因为某种原因，依赖未能成功的安装上去，这个时候则需要手动使用`pip install jieba`命令进行安装。



# 中国三级行政区划分（参考自[百度百科](https://baike.baidu.com/item/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92/1292734)）

| 行政区级别               |                                                              |
| ------------------------ | ------------------------------------------------------------ |
| 一级行政区（省级行政区） | 34个（23个省、5个自治区、4个直辖市、2个特别行政区）          |
| 二级行政区（地级行政区） | 334个（294个地级<u>市</u>、7个<u>地区</u>、30个<u>自治州</u>、3个<u>盟</u>） |
| 三级行政区（县级行政区） | 2876个（987个市辖区、363个县级市、1355个县、117自治县、49个旗、3个自治旗、1个特区、1个林区） |



# 特点

 - 基于jieba分词进行匹配，同时加入了一些额外的匹配逻辑保证了准确率
 - 自带完整的省，市，区三级地名及其经纬度的数据
 - 支持自定义省，市，区映射
 - 输出的是基于pandas的DataFrame类型的表结构，易于理解和使用
 - 封装了简单的绘图功能，可以很方便地进行简单的数据可视化
 - MIT 授权协议



# Get Started

本模块中最主要的方法是cpca.transform，该方法可以输入任意的可迭代类型（如list，pandas的Series类型等），然后将其转换为一个DataFrame，下面演示一个最为简单的使用方法：

    location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
    from cpca import *
    df = transform(location_str)
    df


输出的结果为：

         区    市      省      地址
    0  徐汇区  上海市  上海市   虹漕路461号58号楼5楼
    1  洛江区  泉州市  福建省   万安塘西工业区
    2  朝阳区  北京市  北京市   北苑华贸城

> 注：程序输出的df是一个Pandas的DataFrame类型变量，DataFrame可以非常轻易地转化为csv或者excel文件，如果你对DataFrame不熟悉的话，可以参考Pandas的官方文档：http://pandas.pydata.org/pandas-docs/version/0.20/dsintro.html#dataframe，或者往下翻到"示例与测试用例"大标题，那里我也展示了DataFrame的拼接与转换成csv文件的操作。



尝试着对代码稍加修改（其实就是将transform方法的umap参数置为空字典）：

```
location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
from cpca import *
df = transform(location_str, umap={})
df
```

会发现输出变为：

```
     区    市      省       地址
0  徐汇区  上海市  上海市    虹漕路461号58号楼5楼
1  洛江区  泉州市  福建省    万安塘西工业区
2  朝阳区                   北苑华贸城
```

发现这种情况的原因是中国其实不止一个“朝阳区”，除了北京市有一个“朝阳区”外，长春市也有一个“朝阳区”，这样的话，程序就不知道该把“朝阳区”映射到哪个市。之所以前一段程序能够成功地将“朝阳区”映射成“北京市”，是因为当你不传umap参数的时候，会默认传一个笔者推荐的字典，其内容如下（在cpca.py中）：

```
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
```

你会发现，其中指定了将”朝阳区“映射到北京市，因为笔者在测试数据中发现，数据中的”朝阳区“基本上都是指北京市那个”朝阳区“（原因可能是北京市的”朝阳区“的经济以及知名度要远比长春市的那个”朝阳区“发达）。当然，默认的这个umap并没有囊括中国所有的重名区，因为有的时候，两个重名区在数据中都经常被提及，无法强制指定将某个区映射成固定的市，比如福州市的“鼓楼区”与南京市的“鼓楼区”，都是经常被提及的地名。

看看下面一个例子：

    location_str = ["福建省鼓楼区软件大道89号"]
    from cpca import *
    df = transform(location_str)
    df

输出结果为：

```
     区     市    省       地址
0  鼓楼区         福建省   软件大道89号
```

可以看到，市没有被成功提取出来，并且还会产生一个警告信息：

```
WARNING:root:建议添加到umap中的区有：{'鼓楼区'},有多个市含有相同名称的区
```

当程序发现重名区并且不知道将其映射到哪一个市时，会将其加入警告信息，提示用户最好根据数据给它指定一个市进行映射。

当使用以下代码时就能成功地将“鼓楼区”映射到“福州市”：

```
location_str = ["福建省鼓楼区软件大道89号"]
from cpca import *
df = transform(location_str, umap={"鼓楼区":"福州市"})
df
```

输出结果：

```
     区    市      省      地址
0  鼓楼区  福州市  福建省   软件大道89号
```

好在中国只有在三级行政区存在重名问题，二级与一级行政区的名称都是唯一的。

模块中还自带一些简单绘图工具，可以在地图上将上面输出的数据以热力图的形式画出来.

这个工具依赖folium，为了减小本模块的体积，所以并不会预装这个依赖，在使用之前请使用`pip install folium ` .

代码如下：

    from cpca_drawers import *
    #df为上一段代码输出的df
    draw_locations(df, "df.html")

这一段代码运行结束后会在运行代码的当前目录下生成一个df.html文件，用浏览器打开即可看到
绘制好的地图（如果某条数据'省'，'市'或'区'字段有缺，则会忽略该条数据不进行绘制），速度会比较慢，需要耐心等待，绘制的图像如下：

![绘图展示](https://user-images.githubusercontent.com/23725000/39467918-143b576e-4d63-11e8-9325-8c68651ffcc2.png)



draw_locations函数还可以通过指定path参数来改变输出路径，示例代码如下:

    from cpca_drawers import *
    #在当前目录的父目录生成df.html
    draw_locations(df, "df.html", path="../")

还有更多的绘图工具请参考文档的大标题为“示例与测试用例”的部分。

到这里就你就已经知道了本模块的基本使用了，接下来我会阐明更多细节。

# 数据接口

本模块自带全国省市区的映射关系及其经纬度，如果你只是想使用这个数据的话可以使用如下代码：

```
from chinese_province_city_area_mapper.infrastructure import SuperMap
#地区到市的映射数据库，是一个字典类型（key为区名，value为其所属的市名），注意其中包含重复的区名
SuperMap.area_city_mapper
#重复的区名列表，列表类型，如果区名在这个列表中，说明存在多个同名区，则area_city_mapper的映射是不准确的
SuperMap.rep_areas
#市到省的映射数据库，字典类型（key为市的名称，value为省的名称）
SuperMap.city_province_mapper
#全国省市区的经纬度数据库，字典类型（key为"省,市,区",value为(维度,经度)）
SuperMap.lat_lon_mapper
#获取北京市朝阳区的经纬度
SuperMap.lat_lon_mapper.get("北京市,北京市,朝阳区")
#获得一个地名的级别（即省，市或者区）
SuperMap.getType("江苏省")   #返回"province"，即常量SuperMap.PROVINCE
SuperMap.getType("南京市")   #返回"city"，即常量SuperMap.CITY
SuperMap.getType("海淀区")   #返回"area"，即常量SuperMap.AREA
#省略"省"字也能够识别出来
SuperMap.getType("江苏")

```

# 关于匹配与映射的细节

为了保证匹配与映射的正确性，我做了很多细节上的处理，如果在使用本模块的过程中遇到困惑可以参考这里。

 - 能够匹配到省或者市的缩写，比如将"北京市"缩写为"北京"，"江苏省"缩写为"江苏"，依旧能够匹配到并且能够自动补全为全称，示例代码如下：

```
#测试数据
location_strs = ["江苏省南京市鼓楼区256号", "江苏南京鼓楼区256号"]

from cpca import *
df = transform(location_strs)
df
```

输出的结果为：

```
     区    市     省       地址
0  鼓楼区  南京市  江苏省   256号
1  鼓楼区  南京市  江苏省   256号
```

 - 能够自动检测字符串中匹配到的省，市和区是否是所属关系，如果不是所属关系的话，则会删去优先级较低的（注：如果匹配到的是缩写的话，即将"南京市"缩写为"南京"，则认为优先级较低），如果优先级一样的话，则删除地域范围较小的，示例代码如下：


```
#测试数据，一些故意错乱的地址描述
location_strs = ["静安区南京西路30号", "南京市静安区", "江苏省上海市", "上海市静安区南京西路"]

from cpca import *
df = transform(location_strs)
df
```

输出结果如下：

```
     区     市      省       地址
0  静安区  上海市   上海市    西路30号
1          南京市   江苏省    
2                   江苏省
3  静安区  上海市   上海市    西路
```

分析：第一个测试数据"静安区南京西路"会同时匹配到"静安区"和"南京"两个地域名称，但是静安区是属于上海的，和"南京"相矛盾，而且因为"南京"是"南京市"的缩写，因此优先级比较低，故放弃"南京"这个地域名称。

第二个测试数据匹配到"南京市"和"静安区"两个矛盾的地域名称，而且这两个名称都是全称，优先级相同，所以保留地域范围比较大的，即保留"南京市"而放弃"静安区"。第三个测试数据也是一样的道理。

第四个测试数据中有两个市的名称会被匹配到，一个是"上海市"，还有一个是"南京"，但是因为"上海市"在前面被匹配到了，所以"南京"就会被忽略。

> 注意：从上面的例子你会看到，对于这种地址字段在句子中间出现的情况，模块提取出的"地址"列会有些bug，这个目前暂时解决起来比较麻烦，如果地址数据中有大量这种数据的话，建议不要使用模块提取出的"地址"列


# 示例与测试用例

本仓库放了一份大约一万多条地址描述信息addr.csv，用于测试模块，测试代码如下：



*测试基本功能：*

```
#读取数据
import pandas as pd
origin = pd.read_csv("addr.csv")
#转换
from cpca import *
addr_df = transform(origin["原始地址"], myumap)
#输出
processed = pd.concat([origin, addr_df], axis=1)
processed.to_csv("processed.csv", index=False, encoding="utf-8")
```

注意以上代码运行结束后会打印一句warnning，这些warnning是因为程序无法确定某个区县属于哪个市（因为这些区县存在重名问题而且在umap中又没有指定它属于哪一个市）.

*测试绘图函数1（绘制热力图）：*

 模块中绘制热力图的函数是基于folium编写的，为了减小模块体积，在安装模块时没有安装这些绘图库的依赖，如果需要使用这个函数的话，需要先使用`pip install folium  `安装folium  

```
from cpca_drawers import *
#processed为上一段代码的processed
draw_locations(processed, "processed.html")
```

用浏览器打开"processed.html"文件，发现绘制的局部图像如下（在国内folium的地图显示速度比较慢，所以需要耐心等待地图显示）：

![长三角热力图](https://user-images.githubusercontent.com/23725000/39467928-1e7190ae-4d63-11e8-93c4-39f2b2e5432c.png)

（注意：本模块在绘图时，只绘制那些可以精确地匹配到省市区的地址，对于省市区有一个或多个字段缺失的则会直接忽略）

*测试绘图函数2（绘制echarts热力图）:*

因为在国内folium的地图显示速度太慢了，所以添加了echarts的热力图绘图函数.

在使用本函数之前需要先用如下命令安装它的依赖（为了减少本模块的体积，所以这些依赖不会被自动安装）：

```
pip install pyecharts
pip install echarts-countries-pypkg
pip install pyecharts-snapshot
```

示例代码如下，仍然使用之前的测试数据生成的processed变量：
```
from cpca_drawers import *
echarts_draw(processed, "test.html")
```

该接口的更多参数及其含义如下：
```
def echarts_draw(locations, fileName, path="./", title="地域分布图"
                 , subtitle="location distribute"):
    
    """
    生成地域分布的echarts热力图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param fileName: 生成的html文件的文件名.
    :param path: 生成的html文件的路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    """
```

然后会在当前目录下生成一个test.html文件，用浏览器打开后即可看到图像：

![echarts热力图](https://user-images.githubusercontent.com/23725000/39467908-0d60e3a0-4d63-11e8-8f25-06df97dd2889.png)

*测试绘图函数3(绘制分类信息图)：*

在使用本函数之前需要安装的依赖同上一个绘图函数，如果你是跳过了前面的直接读到这里的话，务必向上翻看一下。

样本分类绘制函数，通过额外传入一个样本的分类信息，能够在地图上以不同的颜色画出属于不同分类的样本散点图，以下代码以“省”作为类别信息绘制分类散点图（可以看到，属于不同省的样本被以不同的颜色标记了出来，这里以“省”作为分类标准只是举个例子，实际应用中可以选取更加有实际意义的分类指标）：

```
from cpca_drawers import *
echarts_cate_draw(processed, processed["省"], "test2.html")
```

然后会在当前目录下生成一个test2.html文件，用浏览器打开后即可看到图像：

![echarts分类散点图](https://user-images.githubusercontent.com/23725000/39467901-0471419a-4d63-11e8-92fd-63bab219a766.png)

该接口更多的参数及其含义如下：

```
def echarts_cate_draw(locations, labels, fileName, path="./"
                      , title="地域分布图", subtitle="location distribute",
                      point_size=7):
    """
    依据分类生成地域分布的echarts散点图的html文件.
    :param locations: 样本的省市区, pandas的dataframe类型.
    :param labels: 长度必须和locations相等, 代表每个样本所属的分类.
    :param fileName: 生成的html文件的文件名.
    :param path: 生成的html文件的路径.
    :param title: 图表的标题
    :param subtitle: 图表的子标题
    :param point_size: 每个散点的大小,如果样本数较少可以考虑设置的大一些
    """
```



# END

如果大家在使用过程中发现一些匹配错误的地址，欢迎提issue来帮助我收集这些错误用例和改善算法，毕竟笔者手头数据有限，难以考虑到所有边界情况
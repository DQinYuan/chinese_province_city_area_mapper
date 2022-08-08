# addressparser
[![PyPI version](https://badge.fury.io/py/addressparser.svg)](https://badge.fury.io/py/addressparser)
[![Downloads](https://pepy.tech/badge/addressparser)](https://pepy.tech/project/addressparser)
[![MIT](https://img.shields.io/badge/MIT-blue.svg)](LICENSE)
![Python3](https://img.shields.io/badge/Python-3.6-red.svg)
![Python2.7](https://img.shields.io/badge/Python-2.7-red.svg)
[![GitHub issues](https://img.shields.io/github/issues/shibing624/addressparser.svg)](https://github.com/shibing624/addressparser/issues)
[![Wechat Group](http://vlog.sfyc.ltd/wechat_everyday/wxgroup_logo.png?imageView2/0/w/60/h/20)](#Contact)


中文地址提取工具，支持中国三级区划地址（省、市、区）提取和级联映射，支持地址目的地热力图绘制。适配python2和python3。


## Feature
#### 地址提取


    ["徐汇区虹漕路461号58号楼5楼", "福建泉州市洛江区万安塘西工业区"]
            ↓ 转换
    |省    |市   |区    |地名                |
    |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
    |福建省|泉州市|洛江区|万安塘西工业区        |

> 注：“地名”列代表去除了省市区之后的具体地名


#### 数据集：中国行政区划地名

数据源：爬取自[国家统计局](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/)，[中华人民共和国民政局全国行政区划查询平台](http://xzqh.mca.gov.cn/map)

数据文件存储在：[addressparser/resources/pca.csv](./addressparser/resources/pca.csv)，数据为[2021年统计用区划代码和城乡划分代码（截止时间：2021-10-31，发布时间：2021-12-30）](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html)

## Demo
http://42.193.145.218/product/address_extraction/

## Install
```
pip install addressparser
```

or

```
git clone https://github.com/shibing624/addressparser.git
cd addressparser
python3 setup.py install
```

## Usage

- 省市区提取

示例[base_demo.py](examples/base_demo.py)

```python

location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
import addressparser
df = addressparser.transform(location_str)
print(df)
```

output:
```
       省     市    区          地名
    0 上海市 上海市  徐汇区     虹漕路461号58号楼5楼
    1 福建省 泉州市  洛江区     万安塘西工业区
    2 北京市 北京市  朝阳区     北苑华贸城
```
> 程序的此处输入`location_str`可以是任意的可迭代类型，如list，tuple，set，pandas的Series类型等;

> 输出的`df`是一个Pandas的DataFrame类型变量，DataFrame可以非常轻易地转化为csv或者excel文件，Pandas的官方文档：http://pandas.pydata.org/pandas-docs/version/0.20/dsintro.html#dataframe


- 带位置索引的省市县提取

示例[pos_sensitive_demo.py](examples/pos_sensitive_demo.py)

```python
location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
import addressparser
df = addressparser.transform(location_str, pos_sensitive=True)
print(df)
```

output:

```
     省    市    区        地名                  省_pos  市_pos 区_pos
0  上海市  上海市  徐汇区  虹漕路461号58号楼5楼   -1     -1      0
1  福建省  泉州市  洛江区  万安塘西工业区         -1      0      3
2  北京市  北京市  朝阳区  北苑华贸城             -1     -1      0
```


- 切词模式的省市区提取

默认采用全文匹配模式，不进行分词，直接全文匹配，这样速度慢，准确率高。

示例[enable_cut_demo.py](examples/enable_cut_demo.py)

```python
location_str = ["浙江省杭州市下城区青云街40号3楼"]
import addressparser
df = addressparser.transform(location_str)
print(df)
```

output:

```
   省       市     区         地名
0  浙江省  杭州市  下城区     青云街40号3楼
```

可以先通过jieba分词，之后做省市区提取及映射，所以我们引入了切词模式，速度很快，使用方法如下:
```python

location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
import addressparser
df = addressparser.transform(location_str, cut=True)
print(df)
```

output:
```
       省     市    区          地名
    0 上海市 上海市  徐汇区     虹漕路461号58号楼5楼
    1 福建省 泉州市  洛江区     万安塘西工业区
    2 北京市 北京市  朝阳区     北苑华贸城
```

但可能会出错，如下所示，这种错误的结果是因为jieba本身就将词给分错了：
```python
location_str = ["浙江省杭州市下城区青云街40号3楼"]
import addressparser
df = addressparser.transform(location_str, cut=True)
print(df)
```

output:

```
     省    市      区    地名
0  浙江省  杭州市  城区  下城区青云街40号3楼
```

> 默认情况下transform方法的cut参数为False，即采用全文匹配的方式，这种方式准确率高，但是速度可能会有慢一点；
> 如果追求速度而不追求准确率的话，建议将cut设为True，使用切词模式。


- 地址经纬度、省市县级联关系查询

示例[find_place_demo.py](examples/find_place_demo.py)

```python
## 查询经纬度信息
from addressparser import latlng
latlng[('北京市','北京市','朝阳区')] #输出('39.95895316640668', '116.52169489108084')

## 查询含有"鼓楼区"的全部地址
from addressparser import area_map
area_map.get_relational_addrs('鼓楼区') #[('江苏省', '南京市', '鼓楼区'), ('江苏省', '徐州市', '鼓楼区'), ('福建省', '福州市', '鼓楼区'), ('河南省', '开封市', '鼓楼区')]
#### 注: city_map可以用来查询含有某个市的全部地址, province_map可以用来查询含有某个省的全部地址

## 查询含有"江苏省", "鼓楼区"的全部地址
from addressparser import province_area_map
province_area_map.get_relational_addrs(('江苏省', '鼓楼区')) # [('江苏省', '南京市', '鼓楼区'), ('江苏省', '徐州市', '鼓楼区')]
```

- 绘制echarts热力图

使用echarts的热力图绘图函数之前需要先用如下命令安装它的依赖（为了减少本模块的体积，所以这些依赖不会被自动安装）：

```
pip install pyecharts==0.5.11
pip install echarts-countries-pypkg
pip install pyecharts-snapshot
```

使用本仓库提供的一万多条地址数据[tests/addr.csv](./tests/addr.csv)测试。

示例[draw_demo.py](examples/draw_demo.py)

```python
#读取数据
import pandas as pd
origin = pd.read_csv("tests/addr.csv")
#转换
import addressparser
addr_df = addressparser.transform(origin["原始地址"])
#输出
processed = pd.concat([origin, addr_df], axis=1)
processed.to_csv("processed.csv", index=False, encoding="utf-8")

from addressparser import drawer
drawer.echarts_draw(processed, "echarts.html")
```

output:
```
1) processed.csv：1万多地址的省市县提取结果
2）echarts.html：echarts热力图
```
浏览器打开`echarts.html`后：

![echarts热力图](./docs/echarts.png)

- 绘制分类信息图


样本分类绘制函数，通过额外传入一个样本的分类信息，能够在地图上以不同的颜色画出属于不同分类的样本散点图，以下代码以“省”作为类别信息绘制分类散点图（可以看到，属于不同省的样本被以不同的颜色标记了出来，这里以“省”作为分类标准只是举个例子，实际应用中可以选取更加有实际意义的分类指标）：

示例[draw_demo.py](examples/draw_demo.py)，接上面示例代码：
```python
from addressparser import drawer
drawer.echarts_cate_draw(processed, processed["省"], "echarts_cate.html")
```

浏览器打开输出的`echarts_cate.html`后：

![echarts分类散点图](./docs/echarts_cate.png)

## Command line usage
- 命令行模式

支持批量提取地址的省市区信息：

示例[cmd_demo.py](examples/cmd_demo.py)

```
python3 -m addressparser address_input.csv -o out.csv

usage: python3 -m addressparser [-h] -o OUTPUT [-c] input
@description:

positional arguments:
  input                 the input file path, file encode need utf-8.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        the output file path.
  -c, --cut             use cut mode.

```
> 输入文件：`address_input.csv`；输出文件：`out.csv`，省市县地址以`\t`间隔，`-c`表示使用切词

## Todo
- [x] bug修复，吉林省、广西省部分地址和上海浦东新区等三级区划地址匹配错误
- [x] 增加定期从民政局官网，统计局官网爬取最新省市县镇村划分的功能，延后，原因是2018年后官网未更新
- [x] 解决路名被误识别为省市名的问题，eg"天津空港经济区环河北路80号空港商务园"
- [x] 添加省市区提取后的级联校验逻辑
- [x] 大批量地址数据，准召率效果评估
- [x] 补充香港、澳门、台湾三级区划地址信息


# Contact

- Issue(建议)：[![GitHub issues](https://img.shields.io/github/issues/shibing624/text2vec.svg)](https://github.com/shibing624/text2vec/issues)
- 邮件我：xuming: xuming624@qq.com
- 微信我：
加我*微信号：xuming624, 备注：个人名称-公司-NLP* 进NLP交流群。

<img src="docs/wechat.jpeg" width="200" />


## Citation

如果你在研究中使用了**addressparser**，请按如下格式引用：

APA:
```latex
Xu, M. Addressparser: Chinese address parser toolkit (Version 0.2.4) [Computer software]. https://github.com/shibing624/addressparser
```

BibTeX:
```latex
@software{Xu_Addressparser_Chinese_address,
author = {Xu, Ming},
title = {{Addressparser: Chinese address parser toolkit}},
url = {https://github.com/shibing624/addressparser},
version = {0.2.4}
}
```

## License


授权协议为 [The Apache License 2.0](/LICENSE)，可免费用做商业用途。请在产品说明中附加addressparser的链接和授权协议。


## Contribute
项目代码还很粗糙，如果大家对代码有所改进，欢迎提交回本项目，在提交之前，注意以下两点：

 - 在`tests`添加相应的单元测试
 - 使用`python -m pytest`来运行所有单元测试，确保所有单测都是通过的

之后即可提交PR。


## Reference

* [chinese_province_city_area_mapper](https://github.com/DQinYuan/chinese_province_city_area_mapper)
* [smartParsePro](https://github.com/wzc570738205/smartParsePro)


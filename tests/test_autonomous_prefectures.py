import pandas as pd
import pytest

import cpca


# Issue #105: 30 autonomous prefectures and 3 leagues.
AUTONOMOUS_PREFECTURES = [
    ('延边朝鲜族自治州', '延边', '吉林省', '222400'),
    ('恩施土家族苗族自治州', '恩施', '湖北省', '422800'),
    ('湘西土家族苗族自治州', '湘西', '湖南省', '433100'),
    ('阿坝藏族羌族自治州', '阿坝', '四川省', '513200'),
    ('甘孜藏族自治州', '甘孜', '四川省', '513300'),
    ('凉山彝族自治州', '凉山', '四川省', '513400'),
    ('黔东南苗族侗族自治州', '黔东南', '贵州省', '522600'),
    ('黔南布依族苗族自治州', '黔南', '贵州省', '522700'),
    ('黔西南布依族苗族自治州', '黔西南', '贵州省', '522300'),
    ('楚雄彝族自治州', '楚雄', '云南省', '532300'),
    ('红河哈尼族彝族自治州', '红河', '云南省', '532500'),
    ('文山壮族苗族自治州', '文山', '云南省', '532600'),
    ('西双版纳傣族自治州', '西双版纳', '云南省', '532800'),
    ('大理白族自治州', '大理', '云南省', '532900'),
    ('德宏傣族景颇族自治州', '德宏', '云南省', '533100'),
    ('怒江傈僳族自治州', '怒江', '云南省', '533300'),
    ('迪庆藏族自治州', '迪庆', '云南省', '533400'),
    ('临夏回族自治州', '临夏', '甘肃省', '622900'),
    ('甘南藏族自治州', '甘南', '甘肃省', '623000'),
    ('海南藏族自治州', '海南', '青海省', '632500'),
    ('海北藏族自治州', '海北', '青海省', '632200'),
    ('海西蒙古族藏族自治州', '海西', '青海省', '632800'),
    ('黄南藏族自治州', '黄南', '青海省', '632300'),
    ('果洛藏族自治州', '果洛', '青海省', '632600'),
    ('玉树藏族自治州', '玉树', '青海省', '632700'),
    ('伊犁哈萨克自治州', '伊犁', '新疆维吾尔自治区', '654000'),
    ('博尔塔拉蒙古自治州', '博尔塔拉', '新疆维吾尔自治区', '652700'),
    ('昌吉回族自治州', '昌吉', '新疆维吾尔自治区', '652300'),
    ('巴音郭楞蒙古自治州', '巴音郭楞', '新疆维吾尔自治区', '652800'),
    ('克孜勒苏柯尔克孜自治州', '克孜勒苏', '新疆维吾尔自治区', '653000'),
    ('兴安盟', '兴安', '内蒙古自治区', '152200'),
    ('锡林郭勒盟', '锡林郭勒', '内蒙古自治区', '152500'),
    ('阿拉善盟', '阿拉善', '内蒙古自治区', '152900'),
]


@pytest.mark.parametrize('full_name,short_name,province,adcode', AUTONOMOUS_PREFECTURES)
def test_autonomous_prefecture_abbreviations(full_name, short_name, province, adcode):
    for name in (short_name, full_name):
        result = cpca.transform([province + name], pos_sensitive=True).iloc[0]
        assert result['省'] == province
        assert result['市'] == full_name
        assert result['adcode'] == adcode
        assert result['地址'] == ''
        assert result['省_pos'] == 0
        assert result['市_pos'] == len(province)


@pytest.mark.parametrize('address,province,city,adcode', [
    ('海南', '海南省', None, '460000'),
    ('海南海口', '海南省', '海口市', '460100'),
    ('海南省海口市', '海南省', '海口市', '460100'),
    ('海南藏族自治州', '青海省', '海南藏族自治州', '632500'),
    ('青海海南', '青海省', '海南藏族自治州', '632500'),
    ('吉林', '吉林省', None, '220000'),
    ('吉林省吉林市', '吉林省', '吉林市', '220200'),
])
def test_abbreviation_collisions(address, province, city, adcode):
    result = cpca.transform([address]).iloc[0]
    assert result['省'] == province
    assert pd.isna(result['市']) if city is None else result['市'] == city
    assert result['adcode'] == adcode


def test_ambiguous_abbreviation_positions():
    result = cpca.transform(['青海海南'], pos_sensitive=True).iloc[0]
    assert result['省_pos'] == 0
    assert result['市_pos'] == 2
    result = cpca.transform(['海南'], pos_sensitive=True,
                            umap={'海南': '632500'}).iloc[0]
    assert result['省'] == '青海省'
    assert result['市'] == '海南藏族自治州'
    assert result['省_pos'] == -1
    assert result['市_pos'] == 0


def test_ambiguous_abbreviation_in_multiple_addresses():
    result = cpca.transform_text_with_addrs('海南海口；海南', pos_sensitive=True,
                                           umap={'海南': '632500'})
    assert result['adcode'].tolist() == ['632500', '460100', '632500']
    assert result['省_pos'].tolist() == [-1, -1, -1]
    assert result['市_pos'].tolist() == [0, 2, 5]


def test_full_place_name_wins_over_embedded_abbreviation():
    result = cpca.transform(['大兴安岭地区', '黑龙江大兴安岭地区'],
                            pos_sensitive=True)
    assert result['省'].tolist() == ['黑龙江省', '黑龙江省']
    assert result['市'].tolist() == ['大兴安岭地区', '大兴安岭地区']
    assert result['adcode'].tolist() == ['232700', '232700']
    assert result['市_pos'].tolist() == [0, 3]
    assert result['地址'].tolist() == ['', '']


@pytest.mark.parametrize('address,province,city,county,adcode', [
    ('五大连池市', '黑龙江省', '黑河市', '五大连池市', '231182'),
    ('梅县区', '广东省', '梅州市', '梅县区', '441403'),
])
def test_complete_name_keeps_its_entire_span(address, province, city, county, adcode):
    result = cpca.transform([address], pos_sensitive=True).iloc[0]
    assert result['省'] == province
    assert result['市'] == city
    assert result['区'] == county
    assert result['adcode'] == adcode
    assert result['地址'] == ''
    assert result['区_pos'] == 0

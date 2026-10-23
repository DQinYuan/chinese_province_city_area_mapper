import ahocorasick
import re


class MatchInfo:

    def __init__(self, attr_infos, start_index, end_index, origin_value) -> None:
        self.attr_infos = attr_infos
        self.start_index = start_index
        self.end_index = end_index
        self.origin_value = origin_value

    def get_match_addr(self, parent_addr, first_adcode=None):
        if parent_addr:
            return next(filter(lambda attr: attr.belong_to(parent_addr), self.attr_infos), None)
        elif first_adcode:
            res = next(filter(lambda attr: attr.adcode == first_adcode, self.attr_infos), None)
            return res if res else self.attr_infos[0]
        else:
            return self.attr_infos[0]

    def get_rank(self):
        return self.attr_infos[0].rank

    def get_one_addr(self):
        return self.attr_infos[0]

    def __repr__(self) -> str:
        return "from {} to {} value {}".format(self.start_index, self.end_index, self.origin_value)


class Matcher:

    # 特殊的简写：自治区、自治州和盟
    special_abbre = {
        "内蒙古自治区": "内蒙古",
        "广西壮族自治区": "广西",
        "西藏自治区": "西藏",
        "新疆维吾尔自治区": "新疆",
        "宁夏回族自治区": "宁夏",
        "延边朝鲜族自治州": "延边",
        "恩施土家族苗族自治州": "恩施",
        "湘西土家族苗族自治州": "湘西",
        "阿坝藏族羌族自治州": "阿坝",
        "甘孜藏族自治州": "甘孜",
        "凉山彝族自治州": "凉山",
        "黔东南苗族侗族自治州": "黔东南",
        "黔南布依族苗族自治州": "黔南",
        "黔西南布依族苗族自治州": "黔西南",
        "楚雄彝族自治州": "楚雄",
        "红河哈尼族彝族自治州": "红河",
        "文山壮族苗族自治州": "文山",
        "西双版纳傣族自治州": "西双版纳",
        "大理白族自治州": "大理",
        "德宏傣族景颇族自治州": "德宏",
        "怒江傈僳族自治州": "怒江",
        "迪庆藏族自治州": "迪庆",
        "临夏回族自治州": "临夏",
        "甘南藏族自治州": "甘南",
        "海南藏族自治州": "海南",
        "海北藏族自治州": "海北",
        "海西蒙古族藏族自治州": "海西",
        "黄南藏族自治州": "黄南",
        "果洛藏族自治州": "果洛",
        "玉树藏族自治州": "玉树",
        "伊犁哈萨克自治州": "伊犁",
        "博尔塔拉蒙古自治州": "博尔塔拉",
        "昌吉回族自治州": "昌吉",
        "巴音郭楞蒙古自治州": "巴音郭楞",
        "克孜勒苏柯尔克孜自治州": "克孜勒苏",
        "兴安盟": "兴安",
        "锡林郭勒盟": "锡林郭勒",
        "阿拉善盟": "阿拉善"
    }

    def __init__(self, stop_re):
        self.ac = ahocorasick.Automaton()
        self.stop_re = stop_re

    def _abbr_name(self, origin_name):
        return Matcher.special_abbre.get(origin_name) or re.sub(self.stop_re, '', origin_name)

    def add_addr_info(self, addr_info):
        # 同名简称保留所有候选；全称使用独立列表，避免简称歧义污染全称。
        # 无上下文时优先较大的行政区，例如“海南”仍优先匹配海南省。
        for name in dict.fromkeys((addr_info.name, self._abbr_name(addr_info.name))):
            info_tuple = self.ac.get(name, None)
            if info_tuple is None:
                info_tuple = (name, [])
                self.ac.add_word(name, info_tuple)
            info_tuple[1].append(addr_info)
            if name != addr_info.name:
                info_tuple[1].sort(key=lambda addr: addr.rank)

    # 增加地址的阶段结束,之后不会再往对象中添加地址
    def complete_add(self):
        self.ac.make_automaton()

    def _get(self, key):
        return self.ac.get(key)

    def iter(self, sentence):
        prev_start_index = None
        prev_match_info = None
        prev_end_index = None
        for end_index, (original_value, attr_infos) in self.ac.iter(sentence):
            # start_index 和 end_index 是左闭右闭的
            start_index = end_index - len(original_value) + 1
            if prev_end_index is not None and end_index <= prev_end_index:
                continue

            cur_match_info = MatchInfo(attr_infos, start_index, end_index, original_value)
            # 如果遇到的是全称, 会匹配到两次, 简称一次, 全称一次,所以要处理下
            if prev_match_info is not None:
                if start_index <= prev_start_index:
                    # 延后输出，完整地名可能包含先出现的较短简称。
                    prev_match_info = cur_match_info
                else:
                    yield prev_match_info
                    prev_match_info = cur_match_info
            else:
                prev_match_info = cur_match_info
            prev_start_index = start_index
            prev_end_index = end_index

        if prev_match_info is not None:
            yield prev_match_info



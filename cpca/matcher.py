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

    # 特殊的简写,主要是几个少数民族自治区
    special_abbre = {
        "内蒙古自治区": "内蒙古",
        "广西壮族自治区": "广西",
        "西藏自治区": "西藏",
        "新疆维吾尔自治区": "新疆",
        "宁夏回族自治区": "宁夏"
    }

    def __init__(self, stop_re):
        self.ac = ahocorasick.Automaton()
        self.stop_re = stop_re

    def _abbr_name(self, origin_name):
        return Matcher.special_abbre.get(origin_name) or re.sub(self.stop_re, '', origin_name)

    def _first_add_addr(self, addr_info):
        abbr_name = self._abbr_name(addr_info.name)
        # 地址名与简写共享一个list
        share_list = []
        self.ac.add_word(abbr_name, (abbr_name, share_list))
        self.ac.add_word(addr_info.name, (addr_info.name, share_list))
        return abbr_name, share_list

    def add_addr_info(self, addr_info):
        # 因为区名可能重复,所以会添加多次
        info_tuple = self.ac.get(addr_info.name, 0) or self._first_add_addr(addr_info)
        info_tuple[1].append(addr_info)

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
                if start_index == prev_start_index:
                    yield cur_match_info
                    prev_match_info = None
                else:
                    yield prev_match_info
                    prev_match_info = cur_match_info
            else:
                prev_match_info = cur_match_info
            prev_start_index = start_index
            prev_end_index = end_index

        if prev_match_info is not None:
            yield prev_match_info



# -*- coding: utf-8 -*-


class TestAddrMap(object):

    from cpca.structures import P,C,A

    addr_map = None

    place = ("江苏省", "淮安市", "清江浦区")
    place1 = ("浙江省", "丽水市", "青田县")
    place2 = ("浙江省", "丽水市", "莲都区")

    @classmethod
    def setup_class(cls):
        from cpca.structures import AddrMap
        cls.addr_map = AddrMap()
        cls.addr_map.append_relational_addr('淮安', cls.place, cls.C)
        cls.addr_map.append_relational_addr('丽水市', cls.place1, cls.C)
        cls.addr_map.append_relational_addr('丽水市', cls.place2, cls.C)

    def test_get_full_name(self):
        full_name = self.addr_map.get_full_name('淮安')
        assert full_name == '淮安市'

    def test_get_relational_addrs(self):
        places = self.addr_map.get_relational_addrs('淮安')
        assert self.place == places[0]

    def test_in(self):
        assert '淮安' in self.addr_map

    def test_is_unique_value(self):
        assert self.addr_map.is_unique_value('淮安') == True
        assert self.addr_map.is_unique_value('丽水市') == False
        assert self.addr_map.is_unique_value('杭州市') == False

    def test_get_value(self):
        assert self.addr_map.get_value("丽水市", self.P) == "浙江省" 



class TestPca(object):

    pca = None
    pca1 = None

    @classmethod
    def setup_class(cls):
        from cpca.structures import Pca
        cls.pca = Pca('安徽省','合肥市', '肥东区', 0, 3, 7)
        cls.pca1 = Pca("浙江省", "丽水市", "青田县")

    def _assert(self, p_name, assert_name):
        assert getattr(self.pca, p_name) == assert_name

        setattr(self.pca, p_name, 'a')

        assert getattr(self.pca, p_name) == 'a'
        setattr(self.pca, p_name, assert_name)

    def test_province(self):
        self._assert('province', '安徽省')
        self._assert('city', '合肥市')
        self._assert('area', '肥东区')

    def test_propertys_dict(self):
        expect_anhui = {"省": "安徽省", "市": "合肥市", "区": "肥东区", "省_pos": 0, "市_pos": 3, "区_pos": 7}
        expect_zhejiang = {"省": "浙江省", "市": "丽水市", "区": "青田县"}
        assert self.pca.propertys_dict(True) == expect_anhui
        assert self.pca1.propertys_dict(False) == expect_zhejiang

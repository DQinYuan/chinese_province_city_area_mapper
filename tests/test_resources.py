# -*- coding: utf-8 -*-


def test_resources_messy_code():
    """确保resources中的文件没有utf8乱码"""
    import re
    pat = re.compile(r'^[\u4e00-\u9fa5|,|\d|\.|\w]+$')
    from pkg_resources import resource_stream
    with resource_stream('cpca.resources', 'pca.csv') as pca_stream:
        from io import TextIOWrapper
        text = TextIOWrapper(pca_stream, encoding='utf8')
        for line in text:
            assert pat.match(line) != None
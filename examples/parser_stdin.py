# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import sys

sys.path.append('..')
import addressparser

if __name__ == '__main__':
    lines = []
    for line in sys.stdin:
        i = line.strip()
        lines.append(i)
    df = addressparser.transform(lines)
    for map_key in zip(lines, df["省"], df["市"], df["区"], df["地名"]):
        print(','.join([i for i in map_key]))

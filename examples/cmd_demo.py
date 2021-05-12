# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import os
import sys

sys.path.append('..')
import addressparser


def parse(addresses):
    """
    Turns address list into province, city, country and street.
    :param addresses: list of address
    :return: list of province, city, country and street
    """
    result = []
    df = addressparser.transform(addresses, open_warning=False, cut=False)

    for map_key in zip(df["省"], df["市"], df["区"], df["地名"]):
        place = map_key[3]
        if not isinstance(place, str):
            place = ''
        result.append('\t'.join([map_key[0], map_key[1], map_key[2], place]))
    return result


if __name__ == '__main__':

    origin_path = os.path.join(os.path.dirname(__file__), '../tests/addr.csv')

    lines = []
    with open(origin_path, 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line.strip())

    print('{} lines in input'.format(len(lines)))
    parsed = parse(lines)
    count = 0
    with open('addr_processed.txt', 'w', encoding='utf-8') as f:
        for i, o in zip(lines, parsed):
            count += 1
            f.write(i + '\t' + o + '\n')
    print('{} lines in output'.format(count))

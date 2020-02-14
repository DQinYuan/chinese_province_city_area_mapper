# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import argparse

import addressparser


def parse(addresses):
    """
    Turns address list into province, city, country and street.
    :param addresses: list of address
    :return: list of province, city, country and street
    """
    result = []
    df = addressparser.transform(addresses, open_warning=False)

    for map_key in zip(df["省"], df["市"], df["区"], df["地址"]):
        result.append('\t'.join([map_key[0], map_key[1], map_key[2], map_key[3]]))
    return result


def main(**kwargs):
    """
    Cmd script of addressparser. Input address file, output extracted province, city country and street.
    :param kwargs: input, a text file object that will be read from. Should contain address data, one address per line
    :param output: a text file object where parsed output will be written. Parsed output will be similar to CSV data
    :type input: text file object in read mode
    :type output: text file object in write mode
    :return:
    """
    lines = []
    with open(kwargs['input'], 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line.strip())

    print('{} lines in input'.format(len(lines)))
    parsed = parse(lines)
    count = 0
    with open(kwargs['output'], 'w', encoding='utf-8') as f:
        for i, o in zip(lines, parsed):
            count += 1
            f.write(i + '\t' + o + '\n')
    print('{} lines in output'.format(count))


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=str,
                        help='the input file path, file encode need utf-8.')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='the output file path.')
    args = parser.parse_args()
    main(**vars(args))


if __name__ == '__main__':
    run()

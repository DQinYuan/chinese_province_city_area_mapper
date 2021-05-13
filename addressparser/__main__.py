# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import argparse
import sys

sys.path.append('..')
import addressparser


def parse(addresses, cut=False):
    """
    Turns address list into province, city, country and street.
    :param addresses: list of address
    :param cut: bool
    :return: list of province, city, country and street
    """
    result = []
    df = addressparser.transform(addresses, open_warning=False, cut=cut)

    for map_key in zip(df["省"], df["市"], df["区"], df["地名"]):
        place = map_key[3]
        if not isinstance(place, str):
            place = ''
        result.append('\t'.join([map_key[0], map_key[1], map_key[2], place]))
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
    cut = kwargs['cut'] if 'cut' in kwargs else False
    parsed = parse(lines, cut=cut)
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
    parser.add_argument('-c', '--cut', action="store_true", help='use cut mode.')
    args = parser.parse_args()
    main(**vars(args))


if __name__ == '__main__':
    run()

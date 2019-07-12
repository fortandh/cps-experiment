# coding: utf-8

import os
import sys
import json

from utils import *

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.mkdir('output')

    input_file_name = sys.argv[1]
    if not os.path.exists(input_file_name):
        print("{} do not exist!".format(input_file_name))
        sys.exit()

    with open(input_file_name, 'r') as input_json, \
         open('output/input.bi', 'w') as output_bi:
        instance = json.load(input_json)
        bigraph = dict_to_bigraph(instance)
        output_bi.write(bigraph)

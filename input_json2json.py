# coding: utf-8

import os
import sys
import json

from bigraph2xmi.models import Entity
from bigraph2xmi.parser import parser
from bigraph2xmi.xml_writer import make_xmi
from utils import *

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.mkdir('output')

    input_file_name = sys.argv[1]
    if not os.path.exists(input_file_name):
        print("{} do not exist!".format(input_file_name))
        sys.exit()

    with open(input_file_name, 'r') as input_json, \
         open('output/goal.json', 'w') as output_json:
        instance = json.load(input_json)
        gm = generate_goals(instance, goal_model, goal_config)
        assign_weight(gm)
        parser.parse(dict_to_bigraph(instance))
        json.dump(gm, output_json, indent=2)

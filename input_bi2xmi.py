# coding: utf-8

import os
import sys

from bigraph2xmi.models import Entity
from bigraph2xmi.parser import parser
from bigraph2xmi.xml_writer import make_xmi

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.mkdir('output')

    input_file_name = sys.argv[1]
    if not os.path.exists(input_file_name):
        print("{} do not exist!".format(input_file_name))
        sys.exit()

    with open(input_file_name, 'r') as input_file, \
         open('output/input.xmi', 'w') as output_file:
        parser.parse(input_file.read())
        output_file.write(str((make_xmi(Entity.instances)), encoding="utf8"))
        

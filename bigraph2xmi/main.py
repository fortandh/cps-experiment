# coding: utf-8

import sys
import os

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if not parent_directory in sys.path:
    sys.path.insert(0, parent_directory)

from bigraph2xmi.models import Entity
from bigraph2xmi.parser import parser
from bigraph2xmi.xml_writer import make_xmi

if __name__ == '__main__':
    with open('input2.bi') as f:
        parser.parse(f.read())
        print(make_xmi(Entity.instances))


# coding: utf-8
from models import Entity
from parser import parser
from xml_writer import make_xmi

if __name__ == '__main__':
    with open('input2.bi') as f:
        parser.parse(f.read())
        print(make_xmi(Entity.instances))


# coding: utf-8
import datetime
import json
import os
from utils import *

from bigraph2xmi.models import Entity
from bigraph2xmi.parser import parser
from bigraph2xmi.xml_writer import make_xmi


if __name__ == '__main__':
    cur_time = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    random.seed(cur_time)
    path = 'layout/{0}'.format(cur_time)
    os.mkdir(path)

    instance = generate_instance(config)
    assign_state(instance, state_config)
    with open('{0}/instance.json'.format(path), 'w') as f:
        json.dump(instance, f, indent=2)

    bigraph = dict_to_bigraph(instance)
    with open('{0}/instance.bi'.format(path), 'w') as f:
        f.write(bigraph)
    with open('{0}/instance.xmi'.format(path), 'w') as f:
        parser.parse(bigraph)
        f.write(str((make_xmi(Entity.instances)), encoding="utf8"))

    gm = generate_goals(instance, goal_model, goal_config)
    assign_weight(gm)
    with open('{0}/goal.json'.format(path), 'w') as f:
        parser.parse(dict_to_bigraph(instance))
        json.dump(gm, f, indent=2)



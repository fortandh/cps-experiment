# coding: utf-8
import random
import copy


config = {
    "Room": 20,
    "Door": 30,  # rooms - 1 <= doors <= doors * (doors - 1) / 2
    "belongings": {  # all belongings <= rooms
        "fixed": {
            "Light": 15,
            "Heater": 15,
            "Window": 8,
            "Printer": 3,
        },
        "movable": {
            "Roomba": 3,
            "Agent": 5,
            "Secretary": 1,
            "Server": 1
        }
    }
}

state_config = {
    "light_on_rate": 0.5,
    "heater_on_rate": 0.5,
    "window_on_rate": 0.5,
    "with_asset_rate": 0.8,
    "clean_rate": 0.2  # other properties can be inferred by state of devices
}

goal_model = {
    "name": "root",
    "weight": 1.0,
    "subs": [{
        "name": "security",
        "weight": None,
        "subs": [{
            "name": "noRoomba",
            "weight": None,
            "subs": []
        }, {
            "name": "assetCollected",
            "weight": None,
            "subs": []
        }, {
            "name": "withSecretary",
            "weight": None,
            "subs": []
        }]
    }, {
        "name": "energyEfficiency",
        "weight": None,
        "subs": [{
            "name": "heaterOff",
            "weight": None,
            "subs": []
        }, {
            "name": "lightOff",
            "weight": None,
            "subs": []
        }]
    }, {
        "name": "usability",
        "weight": None,
        "subs": [{
            "name": "temperatureHigh",
            "weight": None,
            "subs": []
        }, {
            "name": "brightnessHigh",
            "weight": None,
            "subs": []
        }, {
            "name": "clean",
            "weight": None,
            "subs": []
        }]
    }]
}


goal_config = {
    "noRoomba": 0.1,
    "assetCollected": 0.8,
    "withSecretary": 1.0,
    "heaterOff": 0.5,
    "lightOff": 0.5,
    "temperatureHigh": 0.3,
    "brightnessHigh": 0.3,
    "clean": 0.2
}


def distribute(a, b):
    res = []
    cur_a, cur_b = a, b
    for i in range(b):
        if random.random() < float(cur_a) / cur_b:
            cur_a -= 1
            res.append(cur_a)
        else:
            res.append(-1)
        cur_b -= 1
    return res


def random_with_fixed_sum(n, s):
    r = min(s, 1)
    x = random.uniform(max(0, r - (r - s / n) * 2), r)
    return n < 2 and [s] or random.sample([x] + random_with_fixed_sum(n - 1, s - x), n)


def distribute_doors(rooms, doors):
    n_connected, connected = list(range(rooms)), []
    edges = []

    def random_del(l):
        ind = random.randint(0, len(l) - 1)
        return l.pop(ind)

    connected.append(random_del(n_connected))
    while n_connected:
        to_be_con = random_del(n_connected)
        to_be_con2 = connected[random.randint(0, len(connected) - 1)]
        edges.append((to_be_con, to_be_con2) if to_be_con < to_be_con2 else (to_be_con2, to_be_con))
        connected.append(to_be_con)

    hashed = ['{0}.{1}'.format(e[0], e[1]) for e in edges]
    left = [(i, j) for i in range(rooms) for j in range(i + 1, rooms) if '{0}.{1}'.format(i, j) not in hashed]
    distribution = distribute(doors - len(edges), len(left))
    edges += [e for i, e in enumerate(left) if distribution[i] >= 0]
    ret = {i: [] for i in range(rooms)}
    for i, (st, ed) in enumerate(edges):
        ret[st].append(i)
        ret[ed].append(i)
    return ret


def generate_instance(config):
    rooms = config['Room']
    bel = {k: distribute(v, rooms) for k, v in config['belongings']['fixed'].items()}
    doors = distribute_doors(rooms, config['Door'])

    return [{'type': 'Room', 'value': 'r{0}'.format(i), 'subs': [{
        'type': 'Door', 'value': 'd{0}'.format(d), 'subs': []
    } for d in doors[i]] + [{
        'type': k, 'value': None, 'subs': []
    } for k, v in bel.items() if v[i] >= 0]} for i in range(rooms)]


def assign_state(instance, state_config):
    bel = {k: distribute(v, len(instance)) for k, v in config['belongings']['movable'].items()}
    for i, room in enumerate(instance):
        light_state = None
        heater_state = None
        window_state = None
        clean = random.random() < state_config['clean_rate']
        for entity in room['subs']:
            if entity['type'] == 'Light':
                light_state = random.random() < state_config['light_on_rate']
                entity['value'] = 'on' if light_state else 'off'
            elif entity['type'] == 'Heater':
                heater_state = random.random() < state_config['heater_on_rate']
                entity['value'] = 'on' if heater_state else 'off'
            elif entity['type'] == 'Window':
                window_state = random.random() < state_config['window_on_rate']
                entity['value'] = 'on' if window_state else 'off'
            elif entity['type'] == 'Printer':
                printer_state = random.random() < state_config['with_asset_rate']
                if printer_state:
                    entity['subs'].append({'type': 'Asset', 'value': None, 'subs': []})

        for k, v in bel.items():
            if v[i] >= 0:
                room['subs'].append({
                    'type': k,
                    'value': '{0}{1}'.format(k, v[i]) if k in ['Agent', 'Secretary'] else None,
                    'subs': []
                })

        room['subs'].append({'type': 'Brightness',
                             'value': 'high' if window_state or light_state else 'low',
                             'subs': []})
        room['subs'].append({'type': 'Temperature',
                             'value': 'high' if heater_state and not window_state else 'low',
                             'subs': []})
        room['subs'].append({'type': 'Cleanness',
                             'value': 'clean' if clean else 'dirty',
                             'subs': []})


def dict_to_bigraph(instance):

    def parse_entity(e):
        return '{0}{1}{2}'.format(
            e['type'],
            ('[{0}]'.format(e['value'])) if e['value'] else '',
            ('.({0})'.format(' | '.join([parse_entity(s) for s in e['subs']]))) if e['subs'] else ''
        )

    return 'SO.({0})'.format(' | '.join([parse_entity(e) for e in instance]))


def generate_goals(instance, goal_model, goal_config):

    leaves = {k: [] for k in goal_config}
    for room in instance:
        qualifications = {k: k == "clean" for k in goal_config}
        for entity in room['subs']:
            if entity['type'] == 'Light':
                qualifications["lightOff"] = True
                qualifications["brightnessHigh"] = True
            elif entity['type'] == 'Heater':
                qualifications["heaterOff"] = True
                qualifications["temperatureHigh"] = True
            elif entity['type'] == 'Window':
                qualifications["brightnessHigh"] = True
                qualifications["temperatureHigh"] = True
            elif entity['type'] == 'Agent':
                qualifications["noRoomba"] = True
            elif entity['type'] == 'Printer':
                qualifications["assetCollected"] = True
            elif entity['type'] == 'Server':
                qualifications["withSecretary"] = True
        for k in qualifications:
            if qualifications[k] and random.random() < goal_config[k]:
                leaves[k].append(room['value'])

    def add_or_prune(g):
        if not g['subs']:
            g['subs'] = [{
                "name": r,
                "weight": None,
                "subs": []
            } for r in leaves[g['name']]]
            return g
        new_subs = []
        for sub in g['subs']:
            n_sub = add_or_prune(sub)
            if n_sub['subs']:
                new_subs.append(n_sub)
        g['subs'] = new_subs
        return g

    g = copy.deepcopy(goal_model)
    return add_or_prune(g)


def assign_weight(root):
    queue = [root]
    while queue:
        cur = queue.pop()
        if not cur['subs']:
            continue
        weights = random_with_fixed_sum(len(cur['subs']), 1)
        for i, g in enumerate(cur['subs']):
            g['weight'] = weights[i]
            queue.append(g)


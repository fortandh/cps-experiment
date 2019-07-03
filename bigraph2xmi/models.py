# coding: utf-8

from functools import reduce


class Entity(object):

    name_count = 0
    instances = []

    def __init__(self, name=None):
        if not name:
            name = 'anonymous_{entity}_{num}'.format(entity=self.__class__.__name__.lower(), num=self.__class__.name_count)
            self.__class__.name_count = self.__class__.name_count + 1
        self.name = name
        self.id = len(self.__class__.instances)
        self.__class__.instances.append(self)

    def add_sub_entities(self, entities):
        pass

    def __repr__(self):
        return '[{type}]{name}'.format(type=self.__class__.__name__, name=self.name)

    def __str__(self):
        return '//@clazz.{id}'.format(id=self.id)

    def to_dict(self):
        def to_str(attr):
            if isinstance(attr, list):
                return reduce(lambda res, cur: res + (res and ' ') + str(cur), attr, '')
            if isinstance(attr, bool):
                return 'true' if attr else 'false'
            return str(attr)

        return {
            k: to_str(v) for k, v in self.__dict__.items()
            if k not in ['id'] and v is not None
        }


class SmartOffice(object):
    def __init__(self, name=None):
        pass

    def add_sub_entities(self, entities):
        pass


class SwitchDevice(Entity):
    def __init__(self, state):
        self.on = state == 'on'
        super(SwitchDevice, self).__init__()


class Heater(SwitchDevice):
    pass


class Light(SwitchDevice):
    pass


class Window(SwitchDevice):
    pass


class Door(Entity):
    def __init__(self, name=None):
        self.room = []
        super(Door, self).__init__(name)


class Roomba(Entity):
    def __init__(self, name=None):
        self.room = None
        super(Roomba, self).__init__(name)


class Printer(Entity):
    def __init__(self, name=None):
        self.asset = None
        self.room = None
        super(Printer, self).__init__(name)

    def add_sub_entities(self, entities):
        for entity in entities:
            if entity.__class__ in [Asset]:
                self.asset = entity


class Asset(Entity):
    pass


class Server(Entity):
    def __init__(self, name=None):
        self.room = None
        super(Server, self).__init__(name)


class Agent(Entity):
    def __init__(self, name=None):
        self.room = None
        super(Agent, self).__init__(name)


class Secretary(Entity):
    def __init__(self, name=None):
        self.room = None
        super(Secretary, self).__init__(name)


class Property(Entity):
    def __init__(self, value):
        self.value = value
        super(Property, self).__init__()


class Brightness(Property):
    pass


class Temperature(Property):
    pass


class Cleanness(Property):
    pass


class Room(Entity):
    accepted_subs = [
        Door, Window, Heater, Light, Roomba, Printer, Server, Agent, Secretary, Brightness, Temperature, Cleanness
    ]

    def __init__(self, name=None):
        super(Room, self).__init__(name)

    def add_sub_entities(self, entities):
        for entity in entities:
            if entity.__class__ in [Door]:
                setattr(
                    self, entity.__class__.__name__.lower(),
                    getattr(self, entity.__class__.__name__.lower(), []) + [entity]
                )
                entity.room = (getattr(entity, 'room') or []) + [self]
            elif entity.__class__ in [Roomba, Printer, Server, Agent, Secretary]:
                setattr(
                    self, entity.__class__.__name__.lower(),
                    getattr(self, entity.__class__.__name__.lower(), []) + [entity]
                )
                entity.room = self
            elif entity.__class__ in [Window, Heater, Light]:
                setattr(self, entity.__class__.__name__.lower(), entity)
                entity.room = self
            elif isinstance(entity, Property):
                setattr(self, entity.__class__.__name__.lower(), entity)
            else:
                raise Exception('illegal sub entity')


# coding: utf-8
from ply import lex, yacc
from models import *

tokens = (
    'NAME',
    'DOT', 'CONNECTOR',
    'LPAREN', 'RPAREN', 'LSQUARE', 'RSQUARE'
)

# Tokens


t_DOT = r'\.'
t_CONNECTOR = r'\|'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Ignored characters
t_ignore = " \t\r\n"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer


lexer = lex.lex()

# Parsing rules

# dictionary of names
names = {}

entity_name_map = {
    'SO': SmartOffice,
    'Room': Room,
    'Heater': Heater,
    'Light': Light,
    'Window': Window,
    'Roomba': Roomba,
    'Server': Server,
    'Agent': Agent,
    'Secretary': Secretary,
    'Printer': Printer,
    'Asset': Asset,
    'Door': Door,
    'Brightness': Brightness,
    'Temperature': Temperature,
    'Cleanness': Cleanness
}


def p_entity(t):
    '''entity : simple_entity DOT LPAREN entities RPAREN
              | simple_entity'''
    if len(t) >= 3:
        t[1].add_sub_entities(t[4])
    t[0] = t[1]


def p_simple_entity(t):
    '''simple_entity : NAME LSQUARE NAME RSQUARE
                     | NAME'''
    if t[1] not in entity_name_map:
        print("Undefined entity type '%s'" % t[1])
        t[0] = None
    else:
        if t[1] in ['Door', 'Room', 'Server', 'Agent', 'Secretary', 'Roomba', 'Printer', 'Asset']:
            if len(t) >= 3:
                if t[3] in names:
                    t[0] = names[t[3]]
                else:
                    t[0] = entity_name_map[t[1]](t[3])
                    names[t[3]] = t[0]
            else:
                t[0] = entity_name_map[t[1]]()
        else:
            t[0] = entity_name_map[t[1]](None if len(t) < 3 else t[3])


def p_entities(t):
    '''entities : entity
                | entity CONNECTOR entities'''
    t[0] = [t[1]] if len(t) < 3 else [t[1]] + t[3]


def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()

if __name__ == '__main__':
    from models import Entity
    from xml_writer import make_xmi
    with open('small.bi') as f:
        parser.parse(f.read())
        print make_xmi(Entity.instances)

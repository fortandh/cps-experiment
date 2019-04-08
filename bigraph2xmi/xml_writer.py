# coding: utf-8
from lxml import etree

_xmi = 'http://www.omg.org/XMI'
_xsi = 'http://www.w3.org/2001/XMLSchema-instance'
_so = 'http://momot.big.tuwien.ac.at/smart_office/2.0'

ROOT_NAME = '{http://momot.big.tuwien.ac.at/smart_office/2.0}SmartOffice'
NSMAP = {
    'smart_office': _so,
    'xmi': _xmi,
    'xsi': _xsi
}

f = lambda a: lambda b: '{%s}%s' % (a, b)

xmi = f(_xmi)
xsi = f(_xsi)
so = f(_so)


def _merge(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def make_xmi(entities):

    smart_office = etree.Element(ROOT_NAME, nsmap=NSMAP, attrib={
        xsi('schemaLocation'):
            'http://momot.big.tuwien.ac.at/smart_office/1.0 ../metamodel/smart_office.ecore',
        xmi('version'): '2.0'
    })
    for entity in entities:
        etree.SubElement(smart_office, 'clazz', attrib=_merge(
            entity.to_dict(),
            {xsi('type'): 'smart_office:' + entity.__class__.__name__}
        ))
    return etree.tostring(smart_office, xml_declaration=True, encoding='UTF-8', pretty_print=True)

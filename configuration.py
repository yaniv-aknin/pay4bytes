import os
from functools import partial
from ConfigParser import SafeConfigParser

DEVICE_NAME_PATTERN = 'device name pattern'
RECEIVE_TOTAL = 'receive total'
TRANSMIT_TOTAL = 'transmit total'

class Configuration(object):
    def __init__(self):
        self.parser = SafeConfigParser()
        self.path = os.path.expanduser('~/.pay4bytes')
    def __iter__(self):
        for section in self.parser.sections():
            yield ConfigurationProxy(self, section)
    def load(self):
        if not os.path.isfile(self.path):
            self.createDefaultFile()
        self.parser.read(self.path)
    def save(self):
        with file(self.path, 'w') as fileHandle:
            self.parser.write(fileHandle)
    def createDefaultFile(self):
        self.parser.add_section('dialup')
        self.parser.set('dialup', DEVICE_NAME_PATTERN, '^ppp[0-9]+$')
        self.parser.set('dialup', RECEIVE_TOTAL, '0')
        self.parser.set('dialup', TRANSMIT_TOTAL, '0')
        self.save()

class ConfigurationProxy(object):
    def __init__(self, root, section):
        self.root = root
        self.section = section
        for method in ['get', 'getint', 'getfloat', 'set']:
            setattr(self, method,
                    partial(getattr(self.root.parser, method), self.section))
    def __str__(self):
        return self.section
    def __repr__(self):
        return '<ConfigurationProxy for %s>' % (self.section,)

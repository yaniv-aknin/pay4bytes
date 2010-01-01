import os
from functools import partial
from ConfigParser import SafeConfigParser

class Configuration(object):
    def __init__(self):
        self.parser = SafeConfigParser()
        self.path = os.path.expanduser('~/.pay4bytes')
    def load(self):
        if not os.path.isfile(self.path):
            self.createDefaultFile()
        self.parser.read(self.path)
    def save(self):
        with file(self.path, 'w') as fileHandle:
            self.parser.write(fileHandle)
    def createDefaultFile(self):
        self.parser.add_section('dialup')
        self.parser.set('dialup', 'device name pattern', '^ppp[0-9]+$')
        self.parser.set('dialup', 'receive total', '0')
        self.parser.set('dialup', 'transmit total', '0')
        self.save()

import pygtk
pygtk.require('2.0')

from twisted.application.service import Application

from core import Pay4BytesCore

application = Application('pay4bytes Applet')

core = Pay4BytesCore()
core.setServiceParent(application)

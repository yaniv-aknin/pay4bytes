from twisted.application.service import Service
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log

import gtk

from status_icon import StatusIcon
from netdevs import read_network_devices_statistics_map

class Pay4BytesCore(Service):
    IReactorTimeProvider = reactor
    updateInterval = 1
    menuItems = (
                    ('Quit', lambda widget: gtk.main_quit()),
                )
    def __init__(self):
        self.statusIcon = StatusIcon(self.menuItems)
        self.timer = LoopingCall(self.updateStatistics)

    def startService(self):
        Service.startService(self)
        self.statusIcon.show()
        self.timer.start(self.updateInterval).addErrback(log.err)

    def stopService(self):
        Service.stopService(self)
        self.statusIcon.hide()
        self.timer.stop()

    def updateStatistics(self):
        self.statusIcon.updateTooltip(read_network_devices_statistics_map())

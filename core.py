from twisted.application.service import Service
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log

import gtk

from status_icon import StatusIcon
from netdevs import readNetworkDevicesStatisticsMap
from configuration import Configuration
from connections import ConnectionRegistry

class Pay4BytesCore(Service):
    IReactorTimeProvider = reactor
    updateInterval = 1
    menuItems = (
                    ('Quit', lambda widget: reactor.stop()),
                )
    def __init__(self):
        self.statusIcon = StatusIcon(self.menuItems)
        self.configuration = Configuration()
        self.connectionRegistry = ConnectionRegistry()
        self.timer = LoopingCall(self.updateStatistics)

    def startService(self):
        Service.startService(self)
        self.configuration.load()
        self.timer.start(self.updateInterval).addErrback(log.err)
        self.statusIcon.show()

    def stopService(self):
        Service.stopService(self)
        self.statusIcon.hide()
        self.timer.stop()
        self.configuration.save()

    def updateStatistics(self):
        statisticsMap = readNetworkDevicesStatisticsMap()
        self.connectionRegistry.updateConnections(statisticsMap)
        self.statusIcon.updateTooltip(statisticsMap)


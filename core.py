import re

from twisted.application.service import Service
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log

import gtk

from status_icon import StatusIcon
from netdevs import readNetworkDevicesStatisticsMap
from configuration import Configuration, DEVICE_NAME_PATTERN
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
        self.connectionRegistry = None
        self.timer = LoopingCall(self.updateStatistics)
        self.timer.clock = self.IReactorTimeProvider

    def startService(self):
        Service.startService(self)
        self.configuration.load()
        self.connectionRegistry = \
            ConnectionRegistry( self.createConfiguredDeviceMap())
        self.timer.start(self.updateInterval).addErrback(log.err)
        self.statusIcon.show()

    def stopService(self):
        self.statusIcon.hide()
        # HACK: the timer should always be running and there's no need for this
        #        check; however, during development the service might be
        #        uncleanly with the timer not running, and then we'd rather
        #        avoid 'trying to stop a timer which isn't running' exception
        if self.timer.running:
            self.timer.stop()
        self.connectionRegistry.updateConfiguration()
        self.configuration.save()
        Service.stopService(self)

    def updateStatistics(self):
        statisticsMap = readNetworkDevicesStatisticsMap()
        self.connectionRegistry.updateConnections(statisticsMap)
        self.statusIcon.updateTooltip(self.connectionRegistry)

    def createConfiguredDeviceMap(self):
        result = {}
        for configuredDevice in self.configuration:
            pattern = re.compile(configuredDevice.get(DEVICE_NAME_PATTERN))
            result[pattern] = configuredDevice
        return result

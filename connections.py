"""Connections are high-level, stateful objects rendered from periodic device-info samples. A Connection denotes the duration of time that the device was sequentially connected, i.e., that repeated samples of the device map showed the Device to be connected."""

from twisted.internet import reactor
from twisted.python import log

from configuration import RECEIVE_TOTAL, TRANSMIT_TOTAL
from format_sizes import humanReadable

class DeviceNotConfigured(Exception):
    pass

class Connection(object):
    IReactorTimeProvider = reactor
    def __init__(self, configuration, deviceName, currentDeviceStatistics):
        self.name = str(configuration)
        self.deviceName = deviceName
        self.connectedOn = self.IReactorTimeProvider.seconds()
        self.configuration = configuration
        self.currentDeviceStatistics = currentDeviceStatistics
    def __str__(self):
        return '%s: %s' % (self.name, humanReadable(self.totalBytes))
    def updateDeviceStatistics(self, currentDeviceStatistics):
        self.currentDeviceStatistics = currentDeviceStatistics
    @property
    def totalBytes(self):
        return self.configuration.getint(RECEIVE_TOTAL) + \
               self.configuration.getint(TRANSMIT_TOTAL) + \
               self.currentDeviceStatistics.receive.bytes + \
               self.currentDeviceStatistics.transmit.bytes
    def updateConfiguration(self):
        updatedReceiveTotal = self.configuration.getint(RECEIVE_TOTAL) + \
            self.currentDeviceStatistics.receive.bytes
        self.configuration.set(RECEIVE_TOTAL, str(updatedReceiveTotal))
        updatedTransmitTotal = self.configuration.getint(TRANSMIT_TOTAL) + \
            self.currentDeviceStatistics.transmit.bytes
        self.configuration.set(TRANSMIT_TOTAL, str(updatedTransmitTotal))

class ConnectionRegistry(object):
    ConnectionClass = Connection
    def __init__(self, devicePatterns):
        self.connections = {}
        self.unconfiguredDeviceCache = set()
        self.devicePatterns = devicePatterns
    def __iter__(self):
        for connection in self.connections.values():
            yield connection
    def updateDevicePatterns(self, devicePatterns):
        self.unconfiguredDeviceCache = set()
        self.devicePatterns = devicePatterns
    def updateConnections(self, deviceStatisticsMap):
        self.handleNewDevices(deviceStatisticsMap)
        self.handleDisconnections(deviceStatisticsMap)
        self.updateConnectionsStatistics(deviceStatisticsMap)
    def handleNewDevices(self, deviceStatisticsMap):
        newDevices = set(deviceStatisticsMap).difference(self.connections)
        for deviceName in newDevices:
            if deviceName in self.unconfiguredDeviceCache:
                continue
            try:
                self.handleNewDevice(deviceName,
                                     deviceStatisticsMap[deviceName])
            except DeviceNotConfigured:
                self.unconfiguredDeviceCache.add(deviceName)
    def handleNewDevice(self, deviceName, currentDeviceStatistics):
        configurationProxy = self.searchConfigurationForDeviceMatch(deviceName)
        log.msg('new connection: %s (%s)' % (configurationProxy, deviceName))
        self.connections[deviceName] = \
            self.ConnectionClass(
                                 configurationProxy,
                                 deviceName,
                                 currentDeviceStatistics
                                )
    def searchConfigurationForDeviceMatch(self, deviceName):
        for pattern, configurationProxy in self.devicePatterns.iteritems():
            if pattern.search(deviceName):
                return configurationProxy
        raise DeviceNotConfigured(deviceName)
    def handleDisconnections(self, deviceStatisticsMap):
        disconnects = set(self.connections).difference(deviceStatisticsMap)
        for connectionName in disconnects:
            self.handleDisconnect(connectionName)
    def handleDisconnect(self, connectionName):
        log.msg('connection %s disconnected' % (connectionName,))
        self.connections[connectionName].updateConfiguration()
        del(self.connections[connectionName])
    def updateConnectionsStatistics(self, deviceStatisticsMap):
        for connectionName, connection in self.connections.iteritems():
            assert connectionName in deviceStatisticsMap, \
                'handleDisconnections left an unhandled disconnection'
            connection.updateDeviceStatistics(
                deviceStatisticsMap[connectionName]
            )
    def updateConfiguration(self):
        for connection in self:
            connection.updateConfiguration()

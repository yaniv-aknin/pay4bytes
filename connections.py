"""Connections are high-level, stateful objects rendered from periodic device-info samples. A Connection denotes the duration of time that the device was sequentially connected, i.e., that repeated samples of the device map showed the Device to be connected."""

from twisted.python import log

class DeviceNotConfigured(Exception):
    pass

class ConnectionRegistry(object):
    def __init__(self, devicePatterns):
        self.connections = {}
        self.unmatchedDeviceCache = set()
        self.devicePatterns = devicePatterns
    def updateDevicePatterns(self, devicePatterns):
        self.unmatchedDeviceCache = set()
        self.devicePatterns = devicePatterns
    def updateConnections(self, deviceStatisticsMap):
        self.handleNewDevices(deviceStatisticsMap)
        self.handleDisconnections(deviceStatisticsMap)
    def handleDisconnections(self, deviceStatisticsMap):
        disconnects = set(self.connections).difference(deviceStatisticsMap)
        for connectionName in disconnects:
            self.handleDisconnect(connectionName)
    def handleDisconnect(self, connectionName):
        log.msg('connection %s disconnected' % (connectionName,))
        # TODO: write persistent connection data to the configuration
        del(self.connections[connectionName])
    def handleNewDevices(self, deviceStatisticsMap):
        newDevices = set(deviceStatisticsMap).difference(self.connections)
        for deviceName in newDevices:
            if deviceName in self.unmatchedDeviceCache:
                continue
            try:
                self.handleNewDevice(deviceName,
                                     deviceStatisticsMap[deviceName])
            except DeviceNotConfigured:
                self.unmatchedDeviceCache.add(deviceName)
    def handleNewDevice(self, deviceName, currentDeviceStatistics):
        configurationProxy = self.searchConfigurationForDeviceMatch(deviceName)
        log.msg('new connection: %s (%s)' % (configurationProxy, deviceName))
        # TODO: create connection object and update it rather than using None
        self.connections[deviceName] = None
    def searchConfigurationForDeviceMatch(self, deviceName):
        for pattern, configurationProxy in self.devicePatterns.iteritems():
            if pattern.search(deviceName):
                return configurationProxy
        raise DeviceNotConfigured(deviceName)
    def updateConfiguration(self):
        log.msg('updating configuration not implemented')

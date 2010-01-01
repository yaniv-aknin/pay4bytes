"""This module handles Connections, which are higher-level, stateful objects rendered from periodic device-info samples. A connection denotes the duration of time that the device was sequentially connected, i.e., that repeated samples of the device map showed the device to be connected."""

from twisted.python import log

class ConnectionRegistry(object):
    def __init__(self):
        self.connections = {}
    def updateConnections(self, deviceStatisticsMap):
        self.handleNewConnections(deviceStatisticsMap)
        self.handleDisconnections(deviceStatisticsMap)
    def handleDisconnections(self, deviceStatisticsMap):
        disconnects = set(self.connections).difference(deviceStatisticsMap)
        for connectionName in disconnects:
            self.handleDisconnect(connectionName)
    def handleDisconnect(self, connectionName):
        log.msg('connection %s disconnected' % (connectionName,))
        # TODO: write persistent connection data to the configuration
        del(self.connections[connectionName])
    def handleNewConnections(self, deviceStatisticsMap):
        newConnections = set(deviceStatisticsMap).difference(self.connections)
        for connectionName in newConnections:
            self.handleNewConnection(connectionName,
                                     deviceStatisticsMap[connectionName])
    def handleNewConnection(self, name, currentDeviceStatistics):
        log.msg('new connection ' + name)
        # TODO: create connection object and update it
        self.connections[name] = None

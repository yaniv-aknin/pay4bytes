"""This package defines the NetworkDevicesStatistics class, which implements platform-specific collection of statistics about known network devices and convenient mapping like representation of these statistics.
"""
from collections import namedtuple
import platform
import os
import warnings

Direction = namedtuple('Direction', 'receive transmit')
Statistics = namedtuple('Statistics', 'bytes packets errors dropped fifo frames compressed multicast')


if platform.system() == 'Linux' and os.path.isfile('/proc/net/dev'):
    def readNetworkDevicesStatisticsMap():
        with file('/proc/net/dev') as fileHandle:
            result = {}
            # NOTE: skip the header lines
            fileHandle.readline()
            fileHandle.readline()
            # TODO: it is assumed the format of /proc/net/dev is as expected
            for line in fileHandle:
                device, rawStatistics = line.split(':')
                splitStatistics = [int(datum) for datum in
                                   rawStatistics.split()]
                receive, transmit = splitStatistics[:8], splitStatistics[8:]
                result[device.strip()] = \
                    Direction(receive=Statistics(*receive),
                              transmit=Statistics(*transmit))
            return result
else:
    message = 'readNetworkDevicesStatisticsMap() not implemented on this ' \
              'platform'
    warnings.warn(message)
    def readNetworkDevicesStatisticsMap():
        raise NotImplementedError(message)

"""This package defines the NetworkDevicesStatistics class, which implements platform-specific collection of statistics about known network devices and convenient mapping like representation of these statistics.
"""
from collections import namedtuple
import platform
import os
import warnings

Direction = namedtuple('Direction', 'receive transmit')
Statistics = namedtuple('Statistics', 'bytes packets errors dropped fifo frames compressed multicast')


if platform.system() == 'Linux' and os.path.isfile('/proc/net/dev'):
    def read_network_devices_statistics_map():
        with file('/proc/net/dev') as file_handle:
            result = {}
            # NOTE: skip the header lines
            file_handle.readline()
            file_handle.readline()
            # TODO: it is assumed the format of /proc/net/dev is as expected
            for line in file_handle:
                device, raw_statistics = line.split(':')
                split_statistics = [int(datum) for datum in raw_statistics.split()]
                receive, transmit = split_statistics[:8], split_statistics[8:]
                result[device.strip()] = Direction(receive=Statistics(*receive),
                                                   transmit=Statistics(*transmit))
            return result
else:
    message = 'read_network_devices_statistics() not implemented on this platform'
    warnings.warn(message)
    def read_network_devices_statistics():
        raise NotImplementedError(message)

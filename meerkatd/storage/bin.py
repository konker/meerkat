#
# storage.bin
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import time
from struct import pack, unpack
import logging

from storage import BaseStorage

"""
Implements storage of data records in a flat file with a binary format.
Record format:
    Name          Size            Type                Description
    ______________________________________________________________________________ 
    <channel_id>: 1 byte:         byte:               channel id
    <timestamp>:  8 bytes:        double float:       microseconds since the epoch packed with 'd'
    <length>:     2 bytes:        unsigned short int: length of data field packed with 'H'
    <data>:       `length` bytes: bytes:              data field 
"""
class Storage(BaseStorage):
    def __init__(self, filename, autoflush=True):
        self.filename = filename
        self.autoflush = autoflush
        try:
            self.fd = open(filename, 'a')
        except IOError as ex:
            logging.error("Storage: Could not open file %s: %s" % (filename, ex))
            raise ex


    def type(self):
        return "bin"


    def write_array(self, channel_id, array):
        channel_id = self._channel_id(channel_id)
        timestamp = self._timestamp()
        length    = self._length(array)

        self.fd.write(channel_id)
        self.fd.write(timestamp)
        self.fd.write(length)
        array.tofile(self.fd)

        if self.autoflush:
            self.fd.flush()


    def write_str(self, channel_id, s):
        channel_id = self._channel_id(channel_id)
        timestamp = self._timestamp()
        length    = self._length(s)

        self.fd.write(channel_id)
        self.fd.write(timestamp)
        self.fd.write(length)
        self.fd.write(s)

        if self.autoflush:
            self.fd.flush()


    def reader(self):
        with open(self.filename, 'r') as rfd:
            while True:
                channel_id = rfd.read(1)
                if channel_id == '': break

                timestamp = rfd.read(8)
                if timestamp == '': break
                timestamp = unpack('d', timestamp)[0]

                length = rfd.read(2)
                if length == '': break
                length = unpack('H', length)[0]

                data = rfd.read(length)
                if data == '': break

                #print "%s, %s, %s, %s" % (channel_id, timestamp, length, data)
                yield (channel_id, timestamp, length, data)


    def close(self):
        self.fd.close()


    def _channel_id(self, channel_id):
        return pack('B', channel_id)


    def _length(self, data):
        return pack('H', len(data))


    def _timestamp(self):
        return pack('d', time.time())



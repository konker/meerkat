#
# storage.sqlite
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import time
import sqlite3
import logging

from storage import BaseStorage

"""
Implements storage of data records in a sqlite3 database.
"""
class Storage(BaseStorage):
    def __init__(self, database, autocommit=True, buffer_size=1):
        self.database = database
        self.autocommit = autocommit
        self.buffer_size = buffer_size
        self.buffer = []

        try:
            self.conn = sqlite3.connect(database)
            # [FIXME: http://stackoverflow.com/questions/3425320/sqlite3-programmingerror-you-must-not-use-8-bit-bytestrings-unless-you-use-a-te ]
            self.conn.text_factory = str
            self.cursor = self.conn.cursor()
            self._ddl()
        except Exception as ex:
            logging.error("Storage: Could not open database %s: %s" % (database, ex))
            raise ex


    def type(self):
        return "sqlite3"


    def write_array(self, probe_id, array):
        self.write_str(probe_id, array.tostring())


    def write_str(self, probe_id, s):
        timestamp = time.time()
        length    = len(s)

        self.buffer.append((probe_id, timestamp, length, sqlite3.Binary(s)))
        if (len(self.buffer) >= self.buffer_size):
            self.cursor.executemany('''INSERT into accessory_data (probe_id, timestamp, length, data)
                                       VALUES (?, ?, ?, ?)''',
                                       self.buffer)
            self.buffer = []

        if self.autocommit:
            self.conn.commit()


    def get_records_by_probe_id(self, probe_id, n=1):
        for row in self.cursor.execute('SELECT * FROM accessory_data where probe_id = ? LIMIT ?', (probe_id, n)):
            yield row


    def reader(self):
        for row in self.cursor.execute('SELECT * FROM accessory_data'):
            yield row


    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()


    def _ddl(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accessory_data
                            (
                               probe_id,    VARCHAR,
                               timestamp    REAL,
                               length       INT,
                               data         BLOB
                            )''')
        self.conn.commit()


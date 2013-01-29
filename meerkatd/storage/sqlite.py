#
# storage.sqlite
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import re
import time
import sqlite3
import logging

from storage import BaseStorage


CREATE_TABLE_RE = re.compile('CREATE TABLE [^\(]+\(', re.IGNORECASE)
END_CREATE_TABLE_RE = re.compile('\)$', re.MULTILINE)
DDL = """CREATE TABLE IF NOT EXISTS probe_data(
             probe_id     VARCHAR,
             timestamp    REAL,
             length       INT,
             data         BLOB);"""


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
        timestamp = time.time() * 1000
        length    = len(s)

        self.buffer.append((probe_id, timestamp, length, sqlite3.Binary(s)))
        if (len(self.buffer) >= self.buffer_size):
            self.cursor.executemany('''INSERT into probe_data (probe_id, timestamp, length, data)
                                       VALUES (?, ?, ?, ?)''',
                                       self.buffer)
            self.buffer = []

        if self.autocommit:
            self.conn.commit()


    def get_records_by_probe_id(self, probe_id, n=-1):
        if n > 0:
            sql = 'SELECT * FROM probe_data where probe_id = ? ORDER BY timestamp DESC LIMIT ?'
            args = (probe_id, n)
        else:
            sql = 'SELECT * FROM probe_data where probe_id = ? ORDER BY timestamp DESC'
            args = (probe_id,)

        for row in self.cursor.execute(sql, args):
            yield row


    def get_records_by_table(self, table, n=-1):
        if n > 0:
            sql = "SELECT * FROM %s = ? ORDER BY timestamp DESC LIMIT ?" % table
            args = (n,)
        else:
            sql = "SELECT * FROM %s ORDER BY timestamp DESC" % table
            args = ()

        for row in self.cursor.execute(sql, args):
            yield row


    def get_fields(self, table):
        sql = "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = ?"
        args = (table,)
        self.cursor.execute(sql, args)
        r = self.cursor.fetchone()

        fields = END_CREATE_TABLE_RE.sub('', CREATE_TABLE_RE.sub('', r[0])).split(',')
        fields = map(lambda x: x.strip(), fields)
        fields = map(lambda x: x.split()[0], fields)
        return fields


    def reader(self):
        for row in self.cursor.execute('SELECT * FROM probe_data'):
            yield row


    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()


    def _ddl(self):
        self.cursor.execute(DDL)
        self.conn.commit()


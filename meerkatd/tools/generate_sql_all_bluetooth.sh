#!/bin/sh

# bluetooth
tools/generate_sql_bluetooth.py ../../meerkat-data/dbs/rpi1.T1-NT.meerkat.db > ../../meerkat-data/sql/rpi1.T1-NT.bluetooth.sql
tools/generate_sql_bluetooth.py ../../meerkat-data/dbs/rpi2.T1-TA.meerkat.db > ../../meerkat-data/sql/rpi2.T1-TA.bluetooth.sql
tools/generate_sql_bluetooth.py ../../meerkat-data/dbs/rpi3.T2-TA.meerkat.db > ../../meerkat-data/sql/rpi3.T2-TA.bluetooth.sql
tools/generate_sql_bluetooth.py ../../meerkat-data/dbs/rpi2.T2-TA.meerkat.db > ../../meerkat-data/sql/rpi2.T2-TA.bluetooth.sql
tools/generate_sql_bluetooth.py ../../meerkat-data/dbs/rpi1.T3-AF.meerkat.db > ../../meerkat-data/sql/rpi1.T3-AF.bluetooth.sql


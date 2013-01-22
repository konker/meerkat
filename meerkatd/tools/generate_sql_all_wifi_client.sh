#!/bin/sh

# wifi_client
tools/generate_sql_wifi_client.py ../../meerkat-data/dbs/rpi1.T1-NT.meerkat.db > ../../meerkat-data/sql/rpi1.T1-NT.wifi_client.sql
tools/generate_sql_wifi_client.py ../../meerkat-data/dbs/rpi2.T1-TA.meerkat.db > ../../meerkat-data/sql/rpi2.T1-TA.wifi_client.sql
tools/generate_sql_wifi_client.py ../../meerkat-data/dbs/rpi3.T2-TA.meerkat.db > ../../meerkat-data/sql/rpi3.T2-TA.wifi_client.sql
tools/generate_sql_wifi_client.py ../../meerkat-data/dbs/rpi2.T2-TA.meerkat.db > ../../meerkat-data/sql/rpi2.T2-TA.wifi_client.sql
tools/generate_sql_wifi_client.py ../../meerkat-data/dbs/rpi1.T3-AF.meerkat.db > ../../meerkat-data/sql/rpi1.T3-AF.wifi_client.sql


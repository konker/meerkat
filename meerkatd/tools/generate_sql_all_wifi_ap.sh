#!/bin/sh

# wifi_ap
tools/generate_sql_wifi_ap.py ../../meerkat-data/dbs/rpi3.T2-TA.meerkat.db > ../../meerkat-data/sql/rpi3.T2-TA.wifi_ap.sql
tools/generate_sql_wifi_ap.py ../../meerkat-data/dbs/rpi2.T2-TA.meerkat.db > ../../meerkat-data/sql/rpi2.T2-TA.wifi_ap.sql
tools/generate_sql_wifi_ap.py ../../meerkat-data/dbs/rpi1.T3-AF.meerkat.db > ../../meerkat-data/sql/rpi1.T3-AF.wifi_ap.sql


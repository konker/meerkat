#!/bin/sh

sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi1.T1-NT.bluetooth.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi1.T1-NT.wifi_client.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi2.T1-TA.bluetooth.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi2.T1-TA.wifi_client.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi2.T2-TA.bluetooth.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi2.T2-TA.wifi_client.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi2.T2-TA.wifi_ap.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi3.T2-TA.bluetooth.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi3.T2-TA.wifi_client.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi3.T2-TA.wifi_ap.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi1.T3-AF.bluetooth.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi1.T3-AF.wifi_client.sql
sqlite3 ../../meerkat-data/MASTER.db < ../../meerkat-data/sql/rpi1.T3-AF.wifi_ap.sql


-- filter_trial_data_T1-NT-rpi1.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- remove data falling outside T1 NT rpi1 trial

-- T1NTrpi1: 2012-11-26 08:50:37 => 08:50:00 - 1353919800000
--           2012-11-26 12:37:14 => 12:40:00 - 1353933600000

DELETE FROM probe_data WHERE timestamp < 1353919800000;
DELETE FROM probe_data WHERE timestamp > 1353933600000;



-- filter_trial_data_T1-TA-rpi2.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- remove data falling outside T1 TA rpi2 trial

-- T1TArpi2: 2012-11-26 09:37:57 => 09:35:00 - 1353922500000
--           2012-11-26 12:18:23 => 12:20:00 - 1353932400000

DELETE FROM probe_data WHERE timestamp < 1353922500000;
DELETE FROM probe_data WHERE timestamp > 1353932400000;


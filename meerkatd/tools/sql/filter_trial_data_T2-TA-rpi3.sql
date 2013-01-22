-- filter_trial_data_T2-TA-rpi3.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- remove data falling outside T2 TA rpi3 trial

-- T2TArpi3: 2012-12-05 09:09:58 => 09:05:00 - 1354698300000
--           2012-12-05 11:11:29 => 11:15:00 - 1354706100000

DELETE FROM probe_data WHERE timestamp < 1354698300000;
DELETE FROM probe_data WHERE timestamp > 1354706100000;


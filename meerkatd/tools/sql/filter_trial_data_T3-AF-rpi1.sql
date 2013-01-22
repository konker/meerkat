-- filter_trial_data_T3-AF-rpi1.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- remove data falling outside T3 AF rpi1 trial

-- T3AFrpi1: 2012-12-06 07:11:18 => 07:00:00 - 1354777200000
--           2012-12-06 07:50:29 => 08:00:00 - 1354780800000

DELETE FROM probe_data WHERE timestamp < 1354777200000;
DELETE FROM probe_data WHERE timestamp > 1354780800000;


-- add_device_id_rpi2.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- populate device_id field with the value "rpi2"

UPDATE probe_data SET device_id = "rpi2";



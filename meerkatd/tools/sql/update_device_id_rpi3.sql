-- add_device_id_rpi3.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- populate device_id field with the value "rpi3"

UPDATE probe_data SET device_id = "rpi3";



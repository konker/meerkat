-- add_device_id_rpi1.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- populate device_id field with the value "rpi1"

UPDATE probe_data SET device_id = "rpi1";


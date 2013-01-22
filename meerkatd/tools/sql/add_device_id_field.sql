-- add_device_id_field.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- add device_id string field

ALTER TABLE probe_data ADD COLUMN device_id VARCHAR;

-- add_location_id_field.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- add location_id string field

ALTER TABLE probe_data ADD COLUMN location_id VARCHAR;

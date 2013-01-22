-- add_latlong_field.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- add latitude and longitude real fields

ALTER TABLE probe_data ADD COLUMN latitude REAL DEFAULT NULL;
ALTER TABLE probe_data ADD COLUMN longitude REAL DEFAULT NULL;


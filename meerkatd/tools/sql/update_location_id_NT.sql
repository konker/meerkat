-- update_location_id_nt.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- populate location_id field with the value "NT"

UPDATE probe_data SET location_id = "NT";


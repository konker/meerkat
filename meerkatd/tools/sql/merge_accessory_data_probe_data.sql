-- merge_accessory_data_probe_data.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- merge the contents of the table accessory_data into the table probe_data
-- and drop the table accessory_data

BEGIN;
INSERT INTO probe_data SELECT * FROM accessory_data;
COMMIT;

DROP TABLE accessory_data;

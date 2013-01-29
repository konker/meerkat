-- fix_old_probe_data.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- fix the redundant blank column in older probe_data schemas

BEGIN;
-- rename old probe_data table
ALTER TABLE probe_data RENAME TO probe_data_tmp;

-- create a new probe_data table without bad column
CREATE TABLE IF NOT EXISTS probe_data
(
   probe_id     VARCHAR,
   timestamp    REAL,
   length       INT,
   data         BLOB
);

-- transfer the data from old to new tables
INSERT INTO probe_data(probe_id, timestamp, length, data) SELECT probe_id, timestamp, length, data FROM probe_data_tmp;
COMMIT;

-- delete the old table
DROP TABLE probe_data_tmp;


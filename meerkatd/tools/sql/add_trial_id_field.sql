-- add_trial_id_field.sql
--
-- Copyright 2013 Konrad Markus
--
-- Author: Konrad Markus <konker@gmail.com>
--

-- add trial_id string field

ALTER TABLE probe_data ADD COLUMN trial_id VARCHAR;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW eval_observation_complete AS
  SELECT
    eval_observation.id as observation_id,
    is_observation_complete(eval_observation.id) as complete
  FROM eval_observation;

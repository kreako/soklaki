-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW eval_period_current AS
SELECT
  id
FROM eval_period
WHERE
  "start" <= current_date and
  current_date <= "end";

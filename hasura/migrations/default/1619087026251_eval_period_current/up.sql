CREATE OR REPLACE VIEW eval_period_current AS
SELECT
  id
FROM eval_period
WHERE
  "start" <= current_date and
  current_date <= "end";

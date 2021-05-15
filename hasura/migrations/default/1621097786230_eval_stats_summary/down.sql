-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW eval_stats_summary AS
SELECT
  total.period_id as period_id,
  total.cycle as cycle,
  total.total as total,
  COALESCE(observations.total, 0) as observations,
  COALESCE(evaluations.total, 0) as evaluations
FROM (
  SELECT
    period_id,
    cycle,
    COUNT(*) as total
  FROM eval_stats
  GROUP BY cycle, period_id
) as total
LEFT JOIN (
  SELECT
    period_id,
    cycle,
    COUNT(*) as total
  FROM eval_stats
  WHERE observations_count > 0
  GROUP BY cycle, period_id
) as observations
  ON observations.period_id = total.period_id
    AND observations.cycle = total.cycle
LEFT JOIN (
  SELECT
    period_id,
    cycle,
    COUNT(*) as total
  FROM eval_stats
  WHERE evaluations_count > 0
  GROUP BY cycle, period_id
) as evaluations
  ON evaluations.period_id = total.period_id
    AND evaluations.cycle = total.cycle;

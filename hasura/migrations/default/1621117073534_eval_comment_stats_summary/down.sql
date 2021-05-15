-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW eval_comment_stats_summary AS
SELECT
  total.period_id as period_id,
  total.cycle as cycle,
  total.total as total,
  COALESCE(comments.total, 0) as comments
FROM (
  SELECT
    period_id,
    cycle,
    COUNT(*) as total
  FROM eval_comment_stats
  GROUP BY cycle, period_id
) as total
LEFT JOIN (
  SELECT
    period_id,
    cycle,
    COUNT(*) as total
  FROM eval_comment_stats
  WHERE comments_count > 0
  GROUP BY cycle, period_id
) as comments
  ON comments.period_id = total.period_id
    AND comments.cycle = total.cycle;

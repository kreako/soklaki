-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- UPDATE eval_evaluation
--   SET level = CASE
--     WHEN status = 'NotAcquired' THEN 13
--     WHEN status = 'InProgress' THEN 38
--     WHEN status = 'Acquired' THEN 63
--     WHEN status = 'TipTop' THEN 88
--   END
--   WHERE level is null;

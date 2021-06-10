-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW eval_period_weeks AS
SELECT 
    id as eval_period_id,
    generate_series(
        (SELECT date_trunc('week', eval_period.start::date)),
        eval_period.end::date,
        make_interval(days=>7)
    ) as week_start
FROM eval_period;

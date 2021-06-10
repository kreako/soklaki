-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW eval_evaluations_count_period_weeks AS
SELECT
    eval_period.id as eval_period_id,
    eval_period_weeks.week_start,
    eval_evaluation.user_id,
    COUNT(eval_evaluation.id) as evaluations_count
FROM eval_period
JOIN eval_period_weeks
    ON eval_period_weeks.eval_period_id = eval_period.id
JOIN public.user
    ON eval_period.group_id = public.user.group_id
JOIN eval_evaluation_period
    ON eval_evaluation_period.eval_period_id = eval_period.id
JOIN eval_evaluation
    ON eval_evaluation.id = eval_evaluation_period.evaluation_id AND
       eval_evaluation.date >= eval_period_weeks.week_start AND
       eval_evaluation.date < (eval_period_weeks.week_start + make_interval(days=>7)) AND
       eval_evaluation.user_id = public.user.id
GROUP BY
    eval_evaluation.user_id,
    eval_period_weeks.week_start,
    eval_period.id;

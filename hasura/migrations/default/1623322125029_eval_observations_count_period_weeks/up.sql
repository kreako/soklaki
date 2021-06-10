CREATE OR REPLACE VIEW eval_observations_count_period_weeks AS
SELECT
    eval_period.id as eval_period_id,
    eval_period_weeks.week_start,
    eval_observation.user_id,
    COUNT(eval_observation.id) as observations_count
FROM eval_period
JOIN eval_period_weeks
    ON eval_period_weeks.eval_period_id = eval_period.id
JOIN public.user
    ON eval_period.group_id = public.user.group_id
JOIN eval_observation_period
    ON eval_observation_period.eval_period_id = eval_period.id
JOIN eval_observation
    ON eval_observation.id = eval_observation_period.observation_id AND
       eval_observation.date >= eval_period_weeks.week_start AND
       eval_observation.date < (eval_period_weeks.week_start + make_interval(days=>7)) AND
       eval_observation.user_id = public.user.id
GROUP BY
    eval_observation.user_id,
    eval_period_weeks.week_start,
    eval_period.id;

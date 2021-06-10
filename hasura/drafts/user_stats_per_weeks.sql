CREATE OR REPLACE VIEW eval_comments_count_period_weeks AS
SELECT
    eval_period.id as eval_period_id,
    eval_period_weeks.week_start,
    eval_comment.user_id,
    COUNT(eval_comment.id) as comments_count
FROM eval_period
JOIN eval_period_weeks
    ON eval_period_weeks.eval_period_id = eval_period.id
JOIN public.user
    ON eval_period.group_id = public.user.group_id
JOIN eval_comment_period
    ON eval_comment_period.eval_period_id = eval_period.id
JOIN eval_comment
    ON eval_comment.id = eval_comment_period.comment_id AND
       eval_comment.date >= eval_period_weeks.week_start AND
       eval_comment.date < (eval_period_weeks.week_start + make_interval(days=>7)) AND
       eval_comment.user_id = public.user.id
GROUP BY
    eval_comment.user_id,
    eval_period_weeks.week_start,
    eval_period.id


CREATE OR REPLACE VIEW eval_evaluations_count_period_weeks AS
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
    eval_period.id


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
    eval_period.id


CREATE OR REPLACE VIEW eval_period_weeks AS
SELECT 
    id as eval_period_id,
    generate_series(
        (SELECT date_trunc('week', eval_period.start::date)),
        eval_period.end::date,
        make_interval(days=>7)
    ) as week_start
FROM eval_period


with weeks as (
    SELECT generate_series(
        (SELECT date_trunc('week', eval_period.start::date)),
        eval_period.end::date,
        make_interval(days=>7)
    ) as week_start, id, group_id
    FROM eval_period
)
SELECT
    weeks.id as eval_period_id,
    weeks.week_start,
    eval_observation.user_id,
    COUNT(eval_observation.id) as observations_count
FROM weeks
JOIN public.user
    ON weeks.group_id = public.user.group_id
JOIN eval_observation_period
    ON eval_observation_period.eval_period_id = weeks.id
JOIN eval_observation
    ON eval_observation.id = eval_observation_period.observation_id AND
       eval_observation.date >= weeks.week_start AND
       eval_observation.date < (weeks.week_start + make_interval(days=>7)) AND
       eval_observation.user_id = public.user.id
GROUP BY
    eval_observation.user_id,
    weeks.week_start,
    weeks.id

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
    eval_period.id;

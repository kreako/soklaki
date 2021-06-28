-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW "public"."eval_comments_count_period_weeks" AS 
 SELECT eval_period.id AS eval_period_id,
    eval_period_weeks.week_start,
    eval_comment.user_id,
    count(eval_comment.id) AS comments_count
   FROM ((((eval_period
     JOIN eval_period_weeks ON ((eval_period_weeks.eval_period_id = eval_period.id)))
     JOIN "user" ON ((eval_period.group_id = "user".group_id)))
     JOIN eval_comment_period ON ((eval_comment_period.eval_period_id = eval_period.id)))
     JOIN eval_comment ON (((eval_comment.id = eval_comment_period.comment_id) AND (eval_comment.date >= eval_period_weeks.week_start) AND (eval_comment.date < (eval_period_weeks.week_start + make_interval(days => 7))) AND (eval_comment.user_id = "user".id) AND (eval_comment.active = true))))
  GROUP BY eval_comment.user_id, eval_period_weeks.week_start, eval_period.id;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW "public"."eval_evaluations_count_period_weeks" AS 
 SELECT eval_period.id AS eval_period_id,
    eval_period_weeks.week_start,
    eval_evaluation.user_id,
    count(eval_evaluation.id) AS evaluations_count
   FROM ((((eval_period
     JOIN eval_period_weeks ON ((eval_period_weeks.eval_period_id = eval_period.id)))
     JOIN "user" ON ((eval_period.group_id = "user".group_id)))
     JOIN eval_evaluation_period ON ((eval_evaluation_period.eval_period_id = eval_period.id)))
     JOIN eval_evaluation ON (((eval_evaluation.id = eval_evaluation_period.evaluation_id) AND (eval_evaluation.date >= eval_period_weeks.week_start) AND (eval_evaluation.date < (eval_period_weeks.week_start + make_interval(days => 7))) AND (eval_evaluation.user_id = "user".id) AND (eval_evaluation.active = true))))
  GROUP BY eval_evaluation.user_id, eval_period_weeks.week_start, eval_period.id;

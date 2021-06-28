CREATE OR REPLACE VIEW "public"."eval_observations_count_period_weeks" AS 
 SELECT eval_period.id AS eval_period_id,
    eval_period_weeks.week_start,
    eval_observation.user_id,
    count(eval_observation.id) AS observations_count
   FROM ((((eval_period
     JOIN eval_period_weeks ON ((eval_period_weeks.eval_period_id = eval_period.id)))
     JOIN "user" ON ((eval_period.group_id = "user".group_id)))
     JOIN eval_observation_period ON ((eval_observation_period.eval_period_id = eval_period.id)))
     JOIN eval_observation ON (((eval_observation.id = eval_observation_period.observation_id) AND (eval_observation.date >= eval_period_weeks.week_start) AND (eval_observation.date < (eval_period_weeks.week_start + make_interval(days => 7))) AND (eval_observation.user_id = "user".id) AND (eval_observation.active = true))))
  GROUP BY eval_observation.user_id, eval_period_weeks.week_start, eval_period.id;

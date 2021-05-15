-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW public.eval_observation_period AS
SELECT 
   eval_period.id as eval_period_id, 
   eval_observation.id as observation_id 
 FROM eval_period 
 JOIN public.user 
   ON eval_period.group_id = public.user.group_id 
 JOIN eval_observation 
   ON eval_observation.user_id = public.user.id 
     AND eval_observation.date >= eval_period.start 
     AND eval_observation.date <= eval_period.end;

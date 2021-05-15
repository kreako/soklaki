CREATE OR REPLACE VIEW public.eval_evaluation_period AS
SELECT 
   eval_period.id as eval_period_id, 
   eval_evaluation.id as evaluation_id 
 FROM eval_period 
 JOIN public.user 
   ON eval_period.group_id = public.user.group_id 
 JOIN eval_evaluation 
   ON eval_evaluation.user_id = public.user.id 
     AND eval_evaluation.date >= eval_period.start 
     AND eval_evaluation.date <= eval_period.end;

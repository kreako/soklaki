-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW public.eval_comment_period AS
SELECT 
   eval_period.id as eval_period_id, 
   eval_comment.id as comment_id 
 FROM eval_period 
 JOIN public.user 
   ON eval_period.group_id = public.user.group_id 
 JOIN eval_comment 
   ON eval_comment.user_id = public.user.id 
     AND eval_comment.date >= eval_period.start 
     AND eval_comment.date <= eval_period.end;

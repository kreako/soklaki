-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW public.report_period AS
SELECT 
   eval_period.id as eval_period_id, 
   report.id as report_id 
 FROM eval_period 
 JOIN student 
   ON eval_period.group_id = student.group_id 
 JOIN report 
   ON report.student_id = student.id 
     AND report.date >= eval_period.start 
     AND report.date <= eval_period.end;

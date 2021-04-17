-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW "public"."eval_period_student" AS 
SELECT eval_period.id as eval_period_id, student.id as student_id
  FROM eval_period
  LEFT JOIN student ON (
    (student.school_exit is null and student.school_entry <= eval_period.end)
    or
    (student.school_exit is not null and
     student.school_entry <= eval_period.end and
     student.school_exit >= eval_period.start)
  );

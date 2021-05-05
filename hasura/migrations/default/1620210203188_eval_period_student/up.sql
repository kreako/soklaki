CREATE OR REPLACE VIEW "public"."eval_period_student" AS
SELECT eval_period.id as eval_period_id, student.id as student_id, estimate_cycle(eval_period.end, student.birthdate) as cycle
  FROM eval_period
  LEFT JOIN student ON (
    (eval_period.group_id = student.group_id)
    and
    (
      (student.school_exit is null and student.school_entry <= eval_period.end)
      or
      (student.school_exit is not null and
       student.school_entry <= eval_period.end and
       student.school_exit >= eval_period.start)
    )
  );

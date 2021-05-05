SELECT
  eval_period.id as period_id,
  student.id as student_id,
  eval_period_student.cycle as cycle,
  socle_competency.id as competency_id
FROM student
  JOIN eval_period
    ON true
  JOIN eval_period_student
    ON eval_period_student.student_id = student.id
      AND eval_period_student.eval_period_id = eval_period.id
  JOIN socle_competency
    ON socle_competency.cycle::text = eval_period_student.cycle
      AND socle_competency.group_id = eval_period.group_id
WHERE eval_period.id = 945 AND student.id = 837
ORDER BY socle_competency.alpha_full_rank

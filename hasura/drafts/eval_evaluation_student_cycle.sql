CREATE OR REPLACE VIEW eval_evaluation_student_cycle AS
  SELECT
    eval_evaluation.id as evaluation_id,
    student.id as student_id,
    estimate_cycle(eval_evaluation.date, student.birthdate) as cycle
  FROM eval_evaluation
    JOIN student
      ON student.id = eval_evaluation.student_id;
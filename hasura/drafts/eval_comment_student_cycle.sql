CREATE OR REPLACE VIEW eval_comment_student_cycle AS
  SELECT
    eval_comment.id as comment_id,
    student.id as student_id,
    estimate_cycle(eval_comment.date, student.birthdate) as cycle
  FROM eval_comment
    JOIN student
      ON student.id = eval_comment.student_id;
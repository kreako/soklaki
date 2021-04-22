CREATE OR REPLACE VIEW eval_comment_stats AS
SELECT
  eval_period.id as period_id,
  student.id as student_id,
  eval_period_student.cycle as cycle,
  COALESCE(comment.comments_count, 0) as comments_count
FROM student
  JOIN eval_period
    ON true
  JOIN eval_period_student
    ON eval_period_student.student_id = student.id
      AND eval_period_student.eval_period_id = eval_period.id
  LEFT JOIN (
    SELECT
      eval_comment.student_id as student_id,
      eval_comment.eval_period_id as period_id,
      COUNT(id) as comments_count
    FROM eval_comment
    GROUP BY student_id, period_id
  ) as comment
    ON comment.student_id = student.id
      AND comment.period_id = eval_period.id;

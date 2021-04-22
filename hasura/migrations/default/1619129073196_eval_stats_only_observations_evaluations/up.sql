CREATE OR REPLACE VIEW eval_stats AS
SELECT
  eval_period.id as period_id,
  student.id as student_id,
  eval_period_student.cycle as cycle,
  socle_competency.id as competency_id,
  COALESCE(observation.observations_count, 0) as observations_count,
  COALESCE(evaluation.evaluations_count, 0) as evaluations_count
FROM student
  JOIN eval_period
    ON true
  JOIN eval_period_student
    ON eval_period_student.student_id = student.id
      AND eval_period_student.eval_period_id = eval_period.id
  JOIN socle_competency
    ON socle_competency.cycle::text = eval_period_student.cycle
  LEFT JOIN (
    SELECT
      eval_observation_competency.competency_id as competency_id,
      eval_observation_student.student_id as student_id,
      eval_observation.eval_period_id as period_id,
      COUNT(eval_observation_competency.observation_id) as observations_count
    FROM eval_observation_competency
      JOIN eval_observation_student
        ON eval_observation_student.observation_id = eval_observation_competency.observation_id
      JOIN eval_observation
        ON eval_observation.id = eval_observation_competency.observation_id
    GROUP BY competency_id, student_id, period_id
  ) as observation
    ON observation.competency_id = socle_competency.id
      AND observation.student_id = student.id
      AND observation.period_id = eval_period.id
  LEFT JOIN (
    SELECT
      eval_evaluation.student_id as student_id,
      eval_evaluation.competency_id as competency_id,
      eval_evaluation.eval_period_id as period_id,
      COUNT(id) as evaluations_count
    FROM eval_evaluation
    GROUP BY competency_id, student_id, period_id
  ) as evaluation
    ON evaluation.competency_id = socle_competency.id
      AND evaluation.student_id = student.id
      AND evaluation.period_id = eval_period.id
ORDER BY socle_competency.alpha_full_rank;

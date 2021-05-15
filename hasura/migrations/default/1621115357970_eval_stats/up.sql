CREATE OR REPLACE VIEW eval_stats AS
SELECT
  eval_period.id as period_id,
  student.id as student_id,
  eval_period_student.cycle as cycle,
  socle_competency.id as competency_id,
  COALESCE(observation.observations_count, 0) as observations_count,
  COALESCE(evaluation.evaluations_count, 0) as evaluations_count,
  COALESCE(evaluation_status.status, 'Empty') as evaluation_status
FROM student
  JOIN eval_period
    ON true
  JOIN eval_period_student
    ON eval_period_student.student_id = student.id
      AND eval_period_student.eval_period_id = eval_period.id
  JOIN socle_competency
    ON socle_competency.cycle::text = eval_period_student.cycle
      AND socle_competency.group_id = eval_period.group_id

  LEFT JOIN (
    SELECT
      eval_observation_competency.competency_id as competency_id,
      eval_observation_student.student_id as student_id,
      eval_observation_period.eval_period_id as period_id,
      COUNT(eval_observation_competency.observation_id) as observations_count
    FROM eval_observation_competency
      JOIN eval_observation_student
        ON eval_observation_student.observation_id = eval_observation_competency.observation_id
      JOIN eval_observation
        ON eval_observation.id = eval_observation_competency.observation_id
          AND eval_observation.active = true
      JOIN eval_observation_period
        ON eval_observation.id = eval_observation_period.observation_id
    GROUP BY competency_id, student_id, period_id
  ) as observation
    ON observation.competency_id = socle_competency.id
      AND observation.student_id = student.id
      AND observation.period_id = eval_period.id

  LEFT JOIN (
    SELECT
      eval_evaluation.student_id as student_id,
      eval_evaluation.competency_id as competency_id,
      eval_evaluation_period.eval_period_id as period_id,
      COUNT(id) as evaluations_count
    FROM eval_evaluation
      JOIN eval_evaluation_period
        ON eval_evaluation.id = eval_evaluation_period.evaluation_id
    WHERE eval_evaluation.active = true
    GROUP BY competency_id, student_id, period_id
  ) as evaluation
    ON evaluation.competency_id = socle_competency.id
      AND evaluation.student_id = student.id
      AND evaluation.period_id = eval_period.id

  LEFT JOIN (
    -- Select the last status for this (period, student, competency)
    SELECT
      e.student_id as student_id,
      e.competency_id as competency_id,
      e.status as status
    FROM (
      -- if same evaluation date the last updated_at
      SELECT
        e_updated_at.student_id,
        e_updated_at.competency_id,
        max(e_updated_at.updated_at) as updated_at
      FROM ( 
        -- last evaluation date
        SELECT    
          eval_evaluation.student_id,
          eval_evaluation.competency_id,
          max(eval_evaluation.date) AS date
        FROM eval_evaluation    
        WHERE eval_evaluation.active = true
        GROUP BY student_id, competency_id
      ) as e_date 
      JOIN eval_evaluation as e_updated_at 
        ON e_updated_at.student_id = e_date.student_id
          AND e_updated_at.competency_id = e_date.competency_id
          AND e_updated_at.active = true
          AND e_updated_at.date = e_date.date
        GROUP BY e_updated_at.student_id, e_updated_at.competency_id
    ) as ex
    JOIN eval_evaluation as e
      ON e.student_id = ex.student_id
        AND e.competency_id = ex.competency_id
        AND active = true
        AND e.updated_at = ex.updated_at
  ) AS evaluation_status
    ON evaluation_status.competency_id = socle_competency.id 
      AND evaluation_status.student_id = student.id

ORDER BY socle_competency.alpha_full_rank;

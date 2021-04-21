-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW eval_observation_student_cycle AS
  SELECT
    eval_observation.id as observation_id,
    student.id as student_id,
    estimate_cycle(eval_observation.date, student.birthdate) as cycle
  FROM eval_observation
    JOIN eval_observation_student
      ON eval_observation_student.observation_id = eval_observation.id
    JOIN student
      ON student.id = eval_observation_student.student_id;

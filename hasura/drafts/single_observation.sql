SELECT 
    eval_period.id as eval_period_id,
    eval_period.name as eval_period_name,
    eval_observation.id as observation_id,
    eval_observation.text as observation_text,
    eval_observation.date as observation_date,
    public.user.email as user_email
  FROM eval_observation 
  JOIN public.user 
    ON eval_observation.user_id = public.user.id 
  JOIN eval_period 
   ON eval_period.group_id = public.user.group_id
     AND eval_observation.date >= eval_period.start 
     AND eval_observation.date <= eval_period.end 
  WHERE eval_observation.id = 466


SELECT  eval_observation.id,
        eval_observation.text,
        eval_observation.created_at,
        eval_observation.updated_at,
        eval_observation.date,
        eval_observation_complete.complete,
        eval_observation.user_id,
        public.user.email,
        public.user.firstname,
        public.user.lastname,
        eval_period.id,
        eval_period.start,
        eval_period.end,
        eval_period.name
  FROM eval_observation
  JOIN eval_observation_complete
    ON eval_observation.id = eval_observation_complete.observation_id
  JOIN public.user
    ON eval_observation.user_id = public.user.id
  JOIN eval_observation_period
    ON eval_observation.id = eval_observation_period.observation_id
  JOIN eval_period
    ON eval_observation_period.eval_period_id = eval_period.id
  WHERE eval_observation.id = 466



SELECT  eval_observation_student.observation_id,
        eval_observation_student.student_id,
        student.firstname,
        student.lastname,
        student_current_cycle.current_cycle
  FROM eval_observation_student
  JOIN student
    ON student.id = eval_observation_student.student_id
  JOIN student_current_cycle
    ON student_current_cycle.student_id = student.id
  WHERE observation_id = 466


  SELECT eval_observation_competency.competency_id,
          socle_competency.cycle,
          socle_competency.text,
          socle_competency.full_rank
  FROM eval_observation_competency
  JOIN socle_competency
    ON socle_competency.id = eval_observation_competency.competency_id
  WHERE observation_id = 466


ALTER TABLE socle_competency
ALTER COLUMN cycle TYPE TEXT 
USING cycle::text;


SELECT  FROM eval_evaluation
  WHERE student_id = $1 AND competency_id = $2
  ORDER BY date DESC LIMIT 1;


SELECT  eval_observation_subject.subject_id,
        socle_subject.title
  FROM eval_observation_subject
  JOIN socle_subject
    ON eval_observation_subject.subject_id = socle_subject.id
  WHERE observation_id = 466 


SELECT level, comment, date
  FROM eval_evaluation_subject 
  WHERE subject_id = 2 and student_id = 1341
  ORDER BY date DESC LIMIT 1;

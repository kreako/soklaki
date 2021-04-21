SELECT 
   eval_observation_competency.observation_id as observation_id, 
   eval_observation_competency.competency_id as competency_id, 
   eval_observation_student.student_id as student_id, 
   eval_evaluation.id as evaluation_id, 
   eval_evaluation.updated_at as updated_at 
 FROM eval_observation_competency 
 JOIN eval_observation_student 
   ON eval_observation_student.observation_id = eval_observation_competency.observation_id 
 JOIN eval_evaluation 
   ON eval_evaluation.student_id = eval_observation_student.student_id AND eval_evaluation.competency_id = eval_observation_competency.competency_id 
 WHERE eval_observation_competency.observation_id = 126 

 SELECT  
 e.id,  
 e.student_id,  
 e.competency_id 
 FROM ( 
 SELECT student_id, max(updated_at) as updated_at FROM eval_evaluation GROUP BY student_id 
 ) as x join eval_evaluation as e 
 ON x.student_id = e.student_id AND x.updated_at = e.updated_at  


SELECT  
 e.id,  
 e.student_id,  
 e.competency_id 
 FROM ( 
 SELECT student_id, competency_id, max(updated_at) as updated_at FROM eval_evaluation GROUP BY student_id, competency_id 
 ) as x join eval_evaluation as e 
 ON x.student_id = e.student_id AND x.updated_at = e.updated_at


SELECT 
   eval_observation_competency.observation_id as observation_id, 
   eval_observation_competency.competency_id as competency_id, 
   eval_observation_student.student_id as student_id, 
   evaluation.id as evaluation_id
 FROM eval_observation_competency 
 JOIN eval_observation_student 
   ON eval_observation_student.observation_id = eval_observation_competency.observation_id 
 JOIN (
   SELECT e.id, e.student_id, e.competency_id FROM (
     SELECT student_id, competency_id, max(updated_at) AS updated_at
     FROM eval_evaluation
     GROUP BY student_id, competency_id
   ) as ex
   JOIN eval_evaluation as e
     ON ex.student_id = e.student_id AND ex.competency_id = e.competency_id AND ex.updated_at = e.updated_at
 ) AS evaluation
   ON evaluation.student_id = eval_observation_student.student_id AND evaluation.competency_id = eval_observation_competency.competency_id 
 WHERE eval_observation_competency.observation_id = 126 

CREATE OR REPLACE VIEW eval_observation_last_evaluations AS
SELECT 
   eval_observation_competency.observation_id as observation_id, 
   eval_observation_competency.competency_id as competency_id, 
   eval_observation_student.student_id as student_id, 
   evaluation.id as evaluation_id
 FROM eval_observation_competency 
 JOIN eval_observation_student 
   ON eval_observation_student.observation_id = eval_observation_competency.observation_id 
 JOIN (
   SELECT e.id, e.student_id, e.competency_id FROM (
     SELECT student_id, competency_id, max(updated_at) AS updated_at
     FROM eval_evaluation
     GROUP BY student_id, competency_id
   ) as ex
   JOIN eval_evaluation as e
     ON ex.student_id = e.student_id AND ex.competency_id = e.competency_id AND ex.updated_at = e.updated_at
 ) AS evaluation
   ON evaluation.student_id = eval_observation_student.student_id AND evaluation.competency_id = eval_observation_competency.competency_id 
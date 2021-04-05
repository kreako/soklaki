alter table "public"."eval_observation_student" add constraint "eval_observation_student_observation_id_student_id_key" unique ("observation_id", "student_id");

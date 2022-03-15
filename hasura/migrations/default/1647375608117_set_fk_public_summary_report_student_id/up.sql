alter table "public"."summary_report"
  add constraint "summary_report_student_id_fkey"
  foreign key ("student_id")
  references "public"."student"
  ("id") on update restrict on delete restrict;

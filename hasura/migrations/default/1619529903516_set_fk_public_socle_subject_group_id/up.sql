alter table "public"."socle_subject"
  add constraint "socle_subject_group_id_fkey"
  foreign key ("group_id")
  references "public"."group"
  ("id") on update cascade on delete cascade;

alter table "public"."socle_competency"
  add constraint "socle_competency_group_id_fkey"
  foreign key ("group_id")
  references "public"."group"
  ("id") on update cascade on delete cascade;

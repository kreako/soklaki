alter table "public"."socle_competency_template"
  add constraint "socle_competency_template_group_id_fkey"
  foreign key ("group_id")
  references "public"."group"
  ("id") on update cascade on delete cascade;

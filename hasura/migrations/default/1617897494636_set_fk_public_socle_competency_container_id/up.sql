alter table "public"."socle_competency"
  add constraint "socle_competency_container_id_fkey"
  foreign key ("container_id")
  references "public"."socle_container"
  ("id") on update cascade on delete cascade;

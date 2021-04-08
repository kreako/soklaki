alter table "public"."socle_competency"
  add constraint "competency_component_id_fkey"
  foreign key ("component_id")
  references "public"."socle_component"
  ("id") on update cascade on delete cascade;

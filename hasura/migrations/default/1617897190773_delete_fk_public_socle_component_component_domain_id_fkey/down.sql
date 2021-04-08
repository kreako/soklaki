alter table "public"."socle_component"
  add constraint "component_domain_id_fkey"
  foreign key ("domain_id")
  references "public"."socle_domain"
  ("id") on update cascade on delete cascade;

CREATE OR REPLACE VIEW "public"."socle_competency_full_rank" AS 
SELECT
  socle_competency.id as competency_id,
  LPAD(CAST(socle_domain.rank as text), 2, '0') || '.'
    || LPAD(CAST(socle_component.rank as text),2, '0') || '.'
    || LPAD(CAST(socle_competency.rank as text), 2, '0')
    as alpha_full_rank,
  CAST(socle_domain.rank as text) || '.'
    || CAST(socle_component.rank as text) || '.'
    || CAST(socle_competency.rank as text)
    as full_rank
FROM socle_competency
  JOIN socle_component ON socle_component.id = socle_competency.component_id
  JOIN socle_domain ON socle_domain.id = socle_component.domain_id
ORDER BY alpha_full_rank;

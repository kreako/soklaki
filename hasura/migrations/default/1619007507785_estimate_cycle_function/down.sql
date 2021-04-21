-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE FUNCTION estimate_cycle(observation_date DATE, birthdate DATE) 
    RETURNS text  
    LANGUAGE plpgsql 
AS $$ 
DECLARE 
    month integer; 
    scholar_year integer; 
    birth_year integer;
    age integer;
BEGIN 
    month := extract(month from observation_date);
    scholar_year := extract(year from observation_date);
    if month <= 7 then
        -- scholar year begins last year
        scholar_year := scholar_year - 1;
    end if;

    birth_year = extract(year from birthdate);

    -- age in year
    age := scholar_year - birth_year;

    if age < 6 then
        return 'c1';
    elseif age < 9 then
        return 'c2';
    elseif age < 12 then
        return 'c3';
    else
        return 'c4';
    end if;
 END; 
 $$;

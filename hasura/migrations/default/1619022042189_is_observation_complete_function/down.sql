-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE FUNCTION is_observation_complete(_observation_id bigint)
    RETURNS boolean  
    LANGUAGE plpgsql 
AS $$ 
DECLARE 
    student_count integer; 
    _cycle cycle;
    cycle_count integer;
BEGIN 
    -- at least 1 student
    SELECT COUNT(id) from eval_observation_student
        INTO student_count
        WHERE observation_id = _observation_id;

    if student_count = 0 then
        return False;
    end if;

    -- at least 1 competency per cycle
    FOR _cycle IN
        -- Select all different cycles
        SELECT cycle
            FROM eval_observation_student_cycle
            WHERE observation_id = _observation_id
            GROUP BY cycle
    LOOP
        -- Select competency with this cycle and this observation
        SELECT COUNT(cycle)
            FROM eval_observation_competency
            JOIN socle_competency
                ON socle_competency.id = eval_observation_competency.competency_id
            INTO cycle_count
            WHERE observation_id = _observation_id AND cycle = _cycle;
        if cycle_count = 0 then
            -- not enough competency for this cycle
            return False;
        end if;
    END LOOP;

    -- OK seems complete
    return True;
 END; 
 $$;

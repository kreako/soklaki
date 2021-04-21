CREATE OR REPLACE VIEW student_current_cycle AS
  SELECT
    student.id as student_id,
    estimate_cycle(current_date, student.birthdate) as current_cycle
  FROM student;

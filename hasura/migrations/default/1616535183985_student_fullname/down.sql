-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE VIEW student_fullname AS
SELECT CONCAT(firstname, ' ', lastname) AS fullname FROM public.student;

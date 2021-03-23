CREATE VIEW student_fullname AS
SELECT CONCAT(firstname, ' ', lastname) AS fullname FROM public.student;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE OR REPLACE VIEW "public"."student_fullname" AS 
 SELECT id, group_id, concat(student.firstname, ' ', student.lastname) AS fullname
   FROM student;

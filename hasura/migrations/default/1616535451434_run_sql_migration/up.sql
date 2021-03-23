CREATE OR REPLACE VIEW "public"."student_fullname" AS 
 SELECT id, group_id, concat(student.firstname, ' ', student.lastname) AS fullname
   FROM student;

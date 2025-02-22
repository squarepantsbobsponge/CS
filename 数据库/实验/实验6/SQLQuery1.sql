CREATE VIEW S3(SID,SANME,GRADE)
AS select sid,sname,grade
from STUDENTS
where grade=1998

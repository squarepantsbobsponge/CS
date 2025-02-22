use School
alter table CHOICES nocheck constraint FK_CHOICES_STUDENTS
DELETE
from STUDENTS
where grade>1998
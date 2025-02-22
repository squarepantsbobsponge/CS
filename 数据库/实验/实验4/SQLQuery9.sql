use School
alter table CHOICES nocheck constraint FK_CHOICES_STUDENTS
DELETE
from STUDENTS
where sid not in(SELECT distinct sid
				from CHOICES
	)
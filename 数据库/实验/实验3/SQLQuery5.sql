use School
select TEACHERS.tid ,CHOICES.cid
from TEACHERS,CHOICES
where TEACHERS.tid=CHOICES.tid and TEACHERS.salary IS NOT NULL and TEACHERS.salary>=all(select salary
														from TEACHERS
														where salary IS NOT NULL
														)


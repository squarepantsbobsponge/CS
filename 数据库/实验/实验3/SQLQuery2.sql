use School
select sname
from STUDENTS
where STUDENTS.grade in (select grade
                          from STUDENTS
						  where STUDENTS.sid='883794999' or STUDENTS.sid='850955252')
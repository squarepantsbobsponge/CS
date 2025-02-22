use School
select STUDENTS.sid,sname,avg(score)
from STUDENTS,CHOICES,COURSES
where STUDENTS.sid=CHOICES.sid and COURSES.cname='c++'and CHOICES.cid=COURSES.cid and CHOICES.score>(select score
                                                 from CHOICES,STUDENTS,COURSES
												 where STUDENTS.sname='ZNKOO' and STUDENTS.sid=CHOICES.sid and COURSES.cid=CHOICES.cid and COURSES.cname='c++')
group by STUDENTS.sid,sname
having count(sname)>1
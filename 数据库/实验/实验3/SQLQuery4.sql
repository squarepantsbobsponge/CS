use School
select cid,cname,COURSES.hour
from COURSES
where COURSES.hour<=all (select hour
                         from COURSES)


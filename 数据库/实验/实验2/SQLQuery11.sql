use School
select Y.cname
from COURSES AS X,COURSES AS Y
where X.cname='c++' AND Y.hour>X.hour
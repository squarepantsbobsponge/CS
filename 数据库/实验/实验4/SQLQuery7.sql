use School
DELETE 
FROM COURSES
WHERE cid in(select distinct cid
				from COURSES
				where cid not in (SELECT distinct cid
					 FROM CHOICES))
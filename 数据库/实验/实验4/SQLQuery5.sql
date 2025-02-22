use School
UPDATE CHOICES
SET tid=(SELECT tid
        FROM TEACHERS 
		WHERE tname='rnupx'
       )
where tid='200016731'
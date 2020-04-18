select incedents.CITY,incedents.severity, Count(*) as NumberOfHardIncedents
from INCEDENTS 
group by (incedents.CITY,incedents.severity)
having incedents.severity > 2;

select incedents.CITY, ROUND(Count(*)/(select count(ID) from incedents),2)*100||'%' as PrecentOfAll
from INCEDENTS 
group by (incedents.CITY);

SELECT to_char(STARTTIME, 'DD.MM.YYYY') as IncedentsDate,count(*) as Incedents
from INCEDENTS
GROUP BY (to_char(STARTTIME, 'DD.MM.YYYY'))
ORDER BY (to_char(STARTTIME, 'DD.MM.YYYY'));
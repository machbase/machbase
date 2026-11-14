SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.json', 'format=json', 'type.id=LONG',
 'parallel=false') ;

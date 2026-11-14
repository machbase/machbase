SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'header=true',
 'type.id=LONG',
 'type.v=LONG') ;

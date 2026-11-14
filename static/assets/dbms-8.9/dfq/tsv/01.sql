SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.tsv', 'format=tsv', 'header=true',
 'type.id=LONG',
 'type.v=LONG') ;

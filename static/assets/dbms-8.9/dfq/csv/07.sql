SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.csv.gz', 'format=csv', 'compression=gzip',
 'type.v=LONG',
 'parallel=false') ;

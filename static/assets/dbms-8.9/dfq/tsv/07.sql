SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.tsv.gz', 'format=tsv', 'compression=gzip',
 'type.v=LONG',
 'parallel=false') ;

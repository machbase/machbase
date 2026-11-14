SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.json.gz', 'format=json', 'compression=gzip',
 'sample_size=-1',
 'parallel=false') ;

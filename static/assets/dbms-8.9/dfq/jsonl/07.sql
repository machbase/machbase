SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.jsonl.gz', 'format=jsonl', 'compression=gzip',
 'sample_size=-1',
 'parallel=false') ;

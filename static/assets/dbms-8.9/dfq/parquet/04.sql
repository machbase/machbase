SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('format=parquet', 'sources=/srv/dfq/part-1.parquet,/srv/dfq/part-2.parquet',
 'parallel=false') ;

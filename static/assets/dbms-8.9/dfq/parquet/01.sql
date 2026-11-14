SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'parallel=false') ;

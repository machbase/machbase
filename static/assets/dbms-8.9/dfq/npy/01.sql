SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'parallel=false') ;

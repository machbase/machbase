SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor') ;

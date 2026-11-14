SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'type.id=LONG',
 'parallel=false') ;

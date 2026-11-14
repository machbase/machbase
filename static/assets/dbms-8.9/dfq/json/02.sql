SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/wrapped.json', 'format=json', 'records=items',
 'type.id=LONG') ;

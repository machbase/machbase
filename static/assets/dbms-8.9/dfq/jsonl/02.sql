SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/wrapped.jsonl', 'format=jsonl', 'records=items',
 'type.id=LONG') ;

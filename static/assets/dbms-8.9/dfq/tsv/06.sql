SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('format=tsv', 'sources=/srv/dfq/part-1.tsv,/srv/dfq/part-2.tsv',
 'union_by_name=true',
 'filename=true') ;

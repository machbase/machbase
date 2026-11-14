SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('format=csv', 'sources=/srv/dfq/part-1.csv,/srv/dfq/part-2.csv',
 'union_by_name=true',
 'filename=true') ;

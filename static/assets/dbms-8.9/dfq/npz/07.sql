SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/arrays.npz', 'format=npz', 'array=main',
 'source.consistency=strong') ;

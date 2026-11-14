SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/comments.csv',
 'format=csv',
 'skip=1',
 'comment=#',
 'header=false',
 'names=id,v,label',
 'all_varchar=true',
 'type.v=LONG');

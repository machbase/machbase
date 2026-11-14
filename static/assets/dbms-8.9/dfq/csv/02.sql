SELECT id,v
FROM READ('/srv/dfq/no-header.csv', 'format=csv', 'header=false',
 'names=id,v,label,day',
 'type.id=LONG',
 'type.v=LONG') ORDER BY id LIMIT 3;

SELECT id,v
FROM READ('/srv/dfq/no-header.tsv', 'format=tsv', 'header=false',
 'names=id,v,label,day',
 'type.id=LONG',
 'type.v=LONG') ORDER BY id LIMIT 3;

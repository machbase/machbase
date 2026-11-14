SELECT *
FROM READ('/srv/dfq/sensor.tsv',
 'format=tsv',
 'header=true',
 'names=id,v,label,day');

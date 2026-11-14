SELECT *
FROM READ('/srv/dfq/sensor.csv',
 'format=csv',
 'header=true',
 'names=id,v,label,day');

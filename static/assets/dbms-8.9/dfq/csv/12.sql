SELECT *
FROM READ('/srv/dfq/sensor.csv',
 'format=csv',
 'unknown_option=true');

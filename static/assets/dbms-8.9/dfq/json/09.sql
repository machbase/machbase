SELECT *
FROM READ('/srv/dfq/sensor.json',
 'format=json',
 'unknown_option=true');

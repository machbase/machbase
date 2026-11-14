SELECT *
FROM READ('/srv/dfq/sensor.mcap',
 'format=mcap',
 'unknown_option=true');

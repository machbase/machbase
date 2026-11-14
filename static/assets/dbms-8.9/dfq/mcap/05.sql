SELECT *
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'target=topics',
 'mode=data') ;

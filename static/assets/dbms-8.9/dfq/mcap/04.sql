SELECT DATA
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'columns=envelope',
 'target=messages',
 'row=0') ;

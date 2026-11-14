SELECT *
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'mode=inspect',
 'view=arrays') ;

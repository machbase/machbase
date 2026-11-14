SELECT DATA
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'columns=envelope',
 'target=rows',
 'row=0') ;

SELECT DATA
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/records',
 'columns=envelope',
 'target=rows',
 'row=0') ;

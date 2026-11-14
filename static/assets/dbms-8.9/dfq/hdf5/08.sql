SELECT *
FROM READ('/srv/dfq/sensor.h5',
 'format=hdf5',
 'dataset=/records',
 'unknown_option=true');

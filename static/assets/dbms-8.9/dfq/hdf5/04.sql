SELECT C1,C2
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/matrix',
 'parallel=false') ORDER BY C1 LIMIT 3;

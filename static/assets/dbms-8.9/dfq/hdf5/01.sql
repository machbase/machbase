SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/records',
 'parallel=false') ;

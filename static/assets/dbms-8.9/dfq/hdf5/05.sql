SELECT DATASET,KIND,DTYPE,SHAPE
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'mode=inspect',
 'view=datasets') ;

SELECT COLUMN_NAME,SQL_TYPE
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/records',
 'mode=inspect',
 'view=columns') ORDER BY COLUMN_ORDINAL;

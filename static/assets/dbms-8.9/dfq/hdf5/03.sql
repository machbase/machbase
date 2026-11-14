SELECT key,reading
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/records',
 'project.key=id',
 'project.reading=v',
 'type.key=LONG') ORDER BY key LIMIT 3;

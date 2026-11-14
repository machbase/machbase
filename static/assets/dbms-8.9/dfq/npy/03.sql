SELECT key,reading
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'project.key=id',
 'project.reading=v') ORDER BY key LIMIT 3;

SELECT key,reading
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'names=key,reading',
 'type.key=LONG') ORDER BY key LIMIT 3;

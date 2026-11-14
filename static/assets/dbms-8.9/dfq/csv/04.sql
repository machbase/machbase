SELECT key,reading
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'project.key=id',
 'project.reading=v',
 'type.id=LONG') ORDER BY key LIMIT 3;

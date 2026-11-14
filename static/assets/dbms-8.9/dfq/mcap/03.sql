SELECT key,reading
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'project.key=id',
 'project.reading=v',
 'type.reading=DOUBLE') ORDER BY key LIMIT 3;

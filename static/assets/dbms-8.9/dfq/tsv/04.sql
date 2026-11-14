SELECT key,reading
FROM READ('/srv/dfq/sensor.tsv', 'format=tsv', 'project.key=id',
 'project.reading=v',
 'type.id=LONG') ORDER BY key LIMIT 3;

SELECT key,x,first
FROM READ('/srv/dfq/sensor.json', 'format=json', 'project.key=id',
 'project.x=pose.x',
 'project.first=items[0]',
 'type.key=LONG') ORDER BY key LIMIT 3;

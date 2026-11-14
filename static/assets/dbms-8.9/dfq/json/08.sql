SELECT key,position,original_v
FROM READ('/srv/dfq/sensor.json', 'format=json', 'project.key=id',
 'column.position=meta.row',
 'column.original_v=data.v') ORDER BY key LIMIT 3;

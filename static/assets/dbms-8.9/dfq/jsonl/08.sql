SELECT key,position,original_v
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'project.key=id',
 'column.position=meta.row',
 'column.original_v=data.v') ORDER BY key LIMIT 3;

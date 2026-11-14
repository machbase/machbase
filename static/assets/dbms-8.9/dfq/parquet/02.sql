SELECT key,x,first
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'project.key=id',
 'project.x=pose.x',
 'project.first=items[0]') ORDER BY key LIMIT 3;

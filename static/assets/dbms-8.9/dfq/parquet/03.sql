SELECT id,v,filename
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'filename=true',
 'type.id=LONG') LIMIT 3;

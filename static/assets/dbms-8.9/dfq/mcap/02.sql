SELECT id,v,time_ns,seq
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'column.time_ns=meta.mcap.log_time',
 'column.seq=meta.mcap.sequence') ORDER BY id LIMIT 3;

SELECT *
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'target=messages',
 'row=0',
 'mode=raw',
 'raw.representation=message_bytes',
 'raw.chunk_bytes=16') ;

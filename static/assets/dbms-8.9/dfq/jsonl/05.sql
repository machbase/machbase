SELECT *
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'mode=elements',
 'target=rows',
 'row=0',
 'field=items') ;

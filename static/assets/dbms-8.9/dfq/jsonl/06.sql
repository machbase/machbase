SELECT DATA
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'columns=envelope',
 'target=rows',
 'row=0',
 'field=pose') ;

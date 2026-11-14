SELECT DATA
FROM READ('/srv/dfq/sensor.json', 'format=json', 'columns=envelope',
 'target=rows',
 'row=0',
 'field=pose') ;

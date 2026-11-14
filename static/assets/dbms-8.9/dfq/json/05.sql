SELECT *
FROM READ('/srv/dfq/sensor.json', 'format=json', 'mode=elements',
 'target=rows',
 'row=0',
 'field=items') ;

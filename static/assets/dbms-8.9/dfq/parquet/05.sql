SELECT DATA
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'columns=envelope',
 'target=rows',
 'row=0',
 'field=pose') ;

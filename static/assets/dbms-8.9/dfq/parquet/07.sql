SELECT *
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'mode=elements',
 'target=rows',
 'row=0',
 'field=items') ;

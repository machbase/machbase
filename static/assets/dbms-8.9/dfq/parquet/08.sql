SELECT *
FROM READ('/srv/dfq/sensor.parquet',
 'format=parquet',
 'unknown_option=true');

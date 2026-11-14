SELECT COLUMN_NAME,SQL_TYPE
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'mode=inspect',
 'view=columns') ORDER BY COLUMN_ORDINAL;

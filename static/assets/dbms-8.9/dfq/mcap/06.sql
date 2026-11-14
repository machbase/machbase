SELECT COLUMN_NAME,SQL_TYPE
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'mode=inspect',
 'view=columns') ORDER BY COLUMN_ORDINAL;

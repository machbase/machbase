SELECT COLUMN_NAME,SQL_TYPE
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=steps',
 'mode=inspect',
 'view=columns') ORDER BY COLUMN_ORDINAL;

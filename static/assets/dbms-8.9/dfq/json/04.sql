SELECT id,day
FROM READ('/srv/dfq/sensor.json', 'format=json', 'type.day=DATE',
 'dateformat.day=%Y-%m-%d',
 'timezone=UTC') LIMIT 3;

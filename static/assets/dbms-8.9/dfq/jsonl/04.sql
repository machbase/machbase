SELECT id,day
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'type.day=DATE',
 'dateformat.day=%Y-%m-%d',
 'timezone=UTC') LIMIT 3;

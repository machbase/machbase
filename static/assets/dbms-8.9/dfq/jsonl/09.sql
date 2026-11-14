SELECT *
FROM READ('/srv/dfq/sensor.jsonl',
 'format=jsonl',
 'unknown_option=true');

SELECT id,day
FROM READ('/srv/dfq/sensor.tsv', 'format=tsv', 'type.day=DATE',
 'dateformat.day=%Y-%m-%d',
 'sample_size=-1') LIMIT 3;

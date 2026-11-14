SELECT *
FROM READ('/srv/dfq/sensor.tsv',
 'format=tsv',
 'unknown_option=true');

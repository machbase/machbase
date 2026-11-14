SELECT id,LENGTH(label) AS BYTES
FROM READ('/srv/dfq/sensor.tsv', 'format=tsv', 'type.label=TEXT',
 'auto_detect=false',
 'header=true') LIMIT 3;

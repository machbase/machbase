SELECT id,LENGTH(label) AS BYTES
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'type.label=TEXT',
 'auto_detect=false',
 'header=true') LIMIT 3;

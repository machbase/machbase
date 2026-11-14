SELECT id,source_file,line_no
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'column.source_file=meta.source',
 'column.line_no=meta.csv.start_line') LIMIT 3;

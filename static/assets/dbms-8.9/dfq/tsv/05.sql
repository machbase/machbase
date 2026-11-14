SELECT id,source_file,line_no
FROM READ('/srv/dfq/sensor.tsv', 'format=tsv', 'column.source_file=meta.source',
 'column.line_no=meta.csv.start_line') LIMIT 3;

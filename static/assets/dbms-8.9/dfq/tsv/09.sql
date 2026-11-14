SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/locale.tsv',
 'format=tsv',
 'header=true',
 'type.id=LONG',
 'type.v=DOUBLE',
 'decimal_separator=,
 ',
 'thousands=.');

SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/locale.csv',
 'format=csv',
 'delimiter=;',
 'header=true',
 'type.id=LONG',
 'type.v=DOUBLE',
 'decimal_separator=,
 ',
 'thousands=.');

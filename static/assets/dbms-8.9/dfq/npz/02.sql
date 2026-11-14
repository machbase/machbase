SELECT key,reading
FROM READ('/srv/dfq/arrays.npz', 'format=npz', 'array=main',
 'names=key,reading',
 'type.key=LONG') ORDER BY key LIMIT 3;

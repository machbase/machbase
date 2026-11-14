SELECT key,reading
FROM READ('/srv/dfq/arrays.npz', 'format=npz', 'array=main',
 'project.key=id',
 'project.reading=v') ORDER BY key LIMIT 3;

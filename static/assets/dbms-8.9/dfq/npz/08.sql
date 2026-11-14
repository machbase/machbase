SELECT *
FROM READ('/srv/dfq/arrays.npz',
 'format=npz',
 'array=main',
 'unknown_option=true');

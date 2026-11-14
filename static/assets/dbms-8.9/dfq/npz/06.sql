SELECT C1,C2
FROM READ('/srv/dfq/arrays.npz', 'format=npz', 'array=matrix',
 'parallel=false') ORDER BY C1 LIMIT 3;

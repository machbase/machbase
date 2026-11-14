SELECT C1,C2
FROM READ('/srv/dfq/matrix.npy', 'format=npy', 'parallel=false') ORDER BY C1 LIMIT 3;

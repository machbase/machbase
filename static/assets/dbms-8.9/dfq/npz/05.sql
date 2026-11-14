SELECT DATA
FROM READ('/srv/dfq/arrays.npz', 'format=npz', 'array=main',
 'columns=envelope',
 'target=rows',
 'row=0') ;

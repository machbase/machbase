SELECT COUNT(*) AS N
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=steps',
 'parallel=false') ;

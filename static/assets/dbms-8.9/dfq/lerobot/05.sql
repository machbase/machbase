SELECT media_id,path,kind
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=media',
 'columns=native') LIMIT 3;

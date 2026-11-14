SELECT episode_index,"length"
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=episodes',
 'columns=native') ORDER BY episode_index;

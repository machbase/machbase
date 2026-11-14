SELECT episode_index,frame_index,"index"
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=steps',
 'parallel=false') WHERE episode_index=42 ORDER BY "index" LIMIT 3;

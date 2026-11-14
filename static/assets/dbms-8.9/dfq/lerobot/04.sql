SELECT task_index,task
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=tasks',
 'columns=native') ORDER BY task_index;

---
title: Linux service
type: docs
weight: 82
---

Using *systemd* or *supervisord*, you can run and manage machbase-neo process as as system service, so that make it to start automatically when the system boot.

## Using systemd

### Create neo-start.sh

```sh
$ vi neo-start.sh
```

*neo-start.sh*

```sh
#!/bin/bash 
exec /data/machbase-neo serve --host 0.0.0.0 --log-filename /data/log/machbase-neo.log
```

```sh
$ chmod 755 neo-start.sh
```
### Create neo.service

```sh
$ cd /etc/systemd/system
$ sudo vi neo.service
```

*neo.service*
```ini
[Unit]   
Description=neo service   
StartLimitBurst=10   
StartLimitIntervalSec=10   
  
[Service]   
User=machbase   
LimitNOFILE=65535   
ExecStart=/data/neo-start.sh   
ExecStop=/data/machbase-neo shell shutdown   
ExecStartPre=sleep 2   
WorkingDirectory=/data   
Restart=always   
RestartSec=1   
  
[Install]   
WantedBy=multi-user.target   
```

* Modify the `User` and paths according to your environment.

### Activate the service.

```sh
$ sudo chmod 755 neo.service
$ sudo systemctl daemon-reload
```

Make the service to auto-start when host machine re-boot.

```sh
$ sudo systemctl enable neo.service
```

After activating the service, you can control it with the following commands:

```sh
$ sudo systemctl start neo.service
$ sudo systemctl status neo.service
$ sudo systemctl stop neo.service
```

## Using supervisord

### Create neo-start.sh

*neo-start.sh*

```sh
#!/bin/bash 
exec /data/machbase-neo serve --host 0.0.0.0 --log-filename /data/log/machbase-neo.log
```

### Create neo.conf

```sh
$ cd /etc/supervisor/conf.d
$ sudo vi neo.conf
```

```ini
[program:neo]
command=/data/neo-start.sh
priority=10   
autostart=true   
autorestart=true   
environment=HOME=/home/machbase   
stdout_logfile=/data/log/machbase-neo_stdout.log   
stderr_logfile=/data/log/machbase-neo_stderr.log   
user=machbase   
```

* Modify the `user` and paths according to your environment.
* In the above example, the log folder `/data/log` should exist in advance.

### Update Supervisor

```sh
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

After activating the service, you can control machbase-neo with the following commands:
```sh
$ sudo supervisorctl start neo
$ sudo supervisorctl status neo
$ sudo supervisorctl stop neo
```

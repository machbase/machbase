---
title: Linux service
type: docs
weight: 82
---

Using *systemd* or *supervisord*, you can run and manage machbase-neo process as as system service, so that make it to start automatically when the system boot.

## Create start/stop script

**Create neo-start.sh**

```sh
$ vi neo-start.sh
```

Use `serve` command with `--pid <path>` flag to write the process id.

```sh {{linenos=table}}
#!/bin/bash 
exec /data/machbase-neo serve \
    --pid /data/neo.pid \
    --host 0.0.0.0 \
    --log-filename /data/log/machbase-neo.log
```

Change shell script to be executable.

```sh
$ chmod 755 neo-start.sh
```

**Create neo-stop.sh**

```sh
$ vi neo-stop.sh
```
Use the stored pid file to terminate with the `kill` command and wait until the process is completely terminated using the `kill -0` command.

```sh  {{linenos=table}}
#!/bin/bash 
PID=`cat /data/neo.pid`
kill $PID
while kill -0 $PID 2>/dev/null; do
  sleep 1
done
```

```sh
$ chmod 755 neo-stop.sh
```

## systemd

{{% steps %}}

### Create neo.service

```sh
$ cd /etc/systemd/system
$ sudo vi neo.service
```

```ini  {{linenos=table}}
[Unit]   
Description=neo service   
StartLimitBurst=10   
StartLimitIntervalSec=10   
  
[Service]   
User=machbase   
LimitNOFILE=65535   
ExecStart=/data/neo-start.sh
ExecStop=/data/neo-stop.sh
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

### Done

After activating the service, you can control it with the following commands:

```sh
$ sudo systemctl start neo.service
$ sudo systemctl status neo.service
$ sudo systemctl stop neo.service
```
{{% /steps %}}

## supervisord

{{% steps %}}

### Create neo.conf

```sh
$ cd /etc/supervisor/conf.d
$ sudo vi neo.conf
```

```ini  {{linenos=table}}
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

### Update Supervisord

```sh
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

### Done

After activating the service, you can control machbase-neo with the following commands:
```sh
$ sudo supervisorctl start neo
$ sudo supervisorctl status neo
$ sudo supervisorctl stop neo
```

{{% /steps %}}

## PM2

{{% steps %}}

### Create neo-start.sh

```sh
$ vi neo-start.sh
```

```sh  {{linenos=table}}
#!/bin/bash
exec /data/machbase-neo serve --host 0.0.0.0
```
* Logs will be managed by PM2, so the `--log-filename` option is not necessary.

### Executable neo-start.sh

```sh
$ chmod 755 neo-start.sh
```

### Run machbase-neo using PM2.

```sh
$ pm2 start /data/neo-start.sh --name neo --log /data/log/machbase-neo.log
```

Check the status of machbase-neo.
```sh
$ pm2 status neo
```

### Make PM2 to auto-start

* You can skip this process if you have already executed it.

To automatically generate and configuration a startup script just type the command (without sudo) `pm2 startup`:
```sh
$ pm2 startup
[PM2] Init System found: systemd
[PM2] To setup the Startup Script, copy/paste the following command:
sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u machbase --hp /home/machbase
```

Then copy/paste the displayed command onto the terminal:
```sh  {{linenos=table}}
$ sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u machbase --hp /home/machbase
```
Now PM2 will automatically restart at boot.

### Saving the app list

Once you have started all desired apps, save the app list so it will respawn after reboot:
```sh
$ pm2 save
```

### Done

You can control machbase-neo with the following commands:

```sh
$ pm2 start neo
$ pm2 status neo
$ pm2 stop neo
$ pm2 restart neo

$ pm2 logs neo
$ pm2 monit
```

{{% /steps %}}

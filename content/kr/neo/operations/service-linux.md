---
title: Linux 서비스
type: docs
weight: 82
---

*systemd* 또는 *supervisord*를 사용하면 machbase-neo 프로세스를 시스템 서비스로 등록해 부팅 시 자동으로 시작하도록 관리할 수 있습니다.

## 시작/중지 스크립트 작성

**neo-start.sh 생성**

```sh
$ vi neo-start.sh
```

```sh {{linenos=table}}
#!/bin/bash 
exec /data/machbase-neo serve --host 0.0.0.0 --log-filename /data/log/machbase-neo.log
```

```sh
$ chmod 755 neo-start.sh
```

**neo-stop.sh 생성**

```sh
$ vi neo-stop.sh
```

```sh  {{linenos=table}}
#!/bin/bash 
/data/machbase-neo shell shutdown
```

```sh
$ chmod 755 neo-stop.sh
```

## systemd

{{% steps %}}

### neo.service 생성

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

* 환경에 맞게 `User`와 경로를 수정하십시오.

### 서비스 활성화

```sh
$ sudo chmod 755 neo.service
$ sudo systemctl daemon-reload
```

호스트가 재부팅될 때 자동 시작하도록 설정합니다.

```sh
$ sudo systemctl enable neo.service
```

### 완료

서비스를 활성화한 후에는 아래 명령으로 제어할 수 있습니다.

```sh
$ sudo systemctl start neo.service
$ sudo systemctl status neo.service
$ sudo systemctl stop neo.service
```
{{% /steps %}}

## supervisord

{{% steps %}}

### neo.conf 생성

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

* 환경에 맞게 `user`와 경로를 수정하십시오.
* 위 예제에서는 로그 폴더 `/data/log`가 미리 존재해야 합니다.

### Supervisord 업데이트

```sh
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

### 완료

서비스를 활성화한 후에는 다음 명령으로 machbase-neo를 제어할 수 있습니다.
```sh
$ sudo supervisorctl start neo
$ sudo supervisorctl status neo
$ sudo supervisorctl stop neo
```

{{% /steps %}}

## PM2

{{% steps %}}

### neo-start.sh 생성

```sh
$ vi neo-start.sh
```

```sh  {{linenos=table}}
#!/bin/bash
exec /data/machbase-neo serve --host 0.0.0.0
```
* 로그는 PM2가 관리하므로 `--log-filename` 옵션은 필요하지 않습니다.

### neo-start.sh 실행 권한 부여

```sh
$ chmod 755 neo-start.sh
```

### PM2로 machbase-neo 실행

```sh
$ pm2 start /data/neo-start.sh --name neo --log /data/log/machbase-neo.log
```

machbase-neo 상태를 확인합니다.
```sh
$ pm2 status neo
```

### PM2 자동 시작 설정

* 이미 수행했다면 이 과정을 건너뛸 수 있습니다.

시작 스크립트를 자동으로 생성하려면 `pm2 startup` 명령을( sudo 없이 ) 실행하십시오.
```sh
$ pm2 startup
[PM2] Init System found: systemd
[PM2] To setup the Startup Script, copy/paste the following command:
sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u machbase --hp /home/machbase
```

출력된 명령을 복사해 터미널에 붙여넣습니다.
```sh  {{linenos=table}}
$ sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u machbase --hp /home/machbase
```
이제 PM2는 부팅 시 자동으로 재시작됩니다.

### 앱 목록 저장

모든 앱을 실행한 뒤 목록을 저장하면 재부팅 후 자동으로 복원됩니다.
```sh
$ pm2 save
```

### 완료

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

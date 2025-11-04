---
title: 시스템 서비스
weight: 400
---

*systemd* 또는 *supervisord*를 사용하면 fluid 프로세스를 시스템 서비스로 실행하고 관리할 수 있으며 시스템이 시작될 때 fluid 프로세스가 자동으로 시작되도록 할 수 있다.

## 시작/종료 스크립트 생성

**fluid-start.sh 파일을 생성한다.**

```sh
$ vi fluid-start.sh
```

* FLUID server
  ```sh
  #!/bin/bash 
  exec /data/fluid serve --config /data/serve-config.yaml
  ```

* FLUID relay
  ```sh
  #!/bin/bash 
  exec /data/fluid relay --config /data/relay-config.yaml
  ```

```sh
$ chmod 755 fluid-start.sh
```

**fluid-stop.sh 파일을 생성한다.**

```sh
$ vi fluid-stop.sh
```

* Fluid server
  ```sh
  #!/bin/bash 
  kill -9 `ps -aef | grep 'fluid serve' | grep -v grep | awk '{print $2}'`
  ```

* Fluid relay
  ```sh
  #!/bin/bash 
  kill -9 `ps -aef | grep 'fluid relay' | grep -v grep | awk '{print $2}'`
  ```

```sh
$ chmod 755 fluid-stop.sh
```

## systemd

{{% steps %}}

### fluid.service 파일을 생성한다.

```sh
$ cd /etc/systemd/system
$ sudo vi fluid.service
```

```ini
[Unit]   
Description=fluid service   
StartLimitBurst=10   
StartLimitIntervalSec=10   
  
[Service]   
User=machbase   
LimitNOFILE=65535   
ExecStart=/data/fluid-start.sh
ExecStop=/data/fluid-stop.sh
ExecStartPre=sleep 2   
WorkingDirectory=/data   
Restart=always   
RestartSec=1   
  
[Install]   
WantedBy=multi-user.target   
```

* 사용환경에 따라서 'User'와 경로는 수정한다.

### service 활성화

```sh
$ sudo chmod 755 fluid.service
$ sudo systemctl daemon-reload
```

시스템 부팅 후에 자동으로 실행되도록 설정한다.

```sh
$ sudo systemctl enable fluid.service
```

### 완료

service가 활성화된 후에는 아래의 명령으로 서비스를 제어할 수 있다.

```sh
$ sudo systemctl start fluid.service
$ sudo systemctl status fluid.service
$ sudo systemctl stop fluid.service
```
{{% /steps %}}

## supervisord

{{% steps %}}

### fluid.conf 파일을 생성한다.

```sh
$ cd /etc/supervisor/conf.d
$ sudo vi fluid.conf
```

```ini
[program:fluid]
command=/data/fluid-start.sh
priority=10   
autostart=true   
autorestart=true   
stdout_logfile=/data/log/fluid_stdout.log   
stderr_logfile=/data/log/fluid_stderr.log   
user=machbase   
```

* 사용환경에 따라서 'User'와 경로는 수정한다.
* 위의 경우 log folder인 `/data/log`는 미리 생성되어 있어야 한다.

### Supervisord를 갱신한다.

```sh
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

### 완료

service가 활성화된 후에는 아래의 명령으로 서비스를 제어할 수 있다.
```sh
$ sudo supervisorctl start fluid
$ sudo supervisorctl status fluid
$ sudo supervisorctl stop fluid
```

{{% /steps %}}

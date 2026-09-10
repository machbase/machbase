---
title: システムサービス
weight: 400
toc: true
---

*systemd* または *supervisord* を使うと、fluid プロセスをシステムサービスとして実行・管理し、
システムの起動時に自動起動できます。

## 起動・停止スクリプトの作成

**fluid-start.sh を作成します。**

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

**fluid-stop.sh を作成します。**

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

### fluid.service の作成

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

* 実行環境に合わせて 'User' とパスを変更します。

### サービスの有効化

```sh
$ sudo chmod 755 fluid.service
$ sudo systemctl daemon-reload
```

システム起動後に自動実行されるよう設定します。

```sh
$ sudo systemctl enable fluid.service
```

### 完了

有効化後は次のコマンドでサービスを制御できます。

```sh
$ sudo systemctl start fluid.service
$ sudo systemctl status fluid.service
$ sudo systemctl stop fluid.service
```
{{% /steps %}}

## supervisord

{{% steps %}}

### fluid.conf の作成

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

* 実行環境に合わせて 'User' とパスを変更します。
* この例では、ログフォルダー `/data/log` を事前に作成しておく必要があります。

### Supervisord の更新

```sh
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

### 完了

有効化後は次のコマンドでサービスを制御できます。
```sh
$ sudo supervisorctl start fluid
$ sudo supervisorctl status fluid
$ sudo supervisorctl stop fluid
```

{{% /steps %}}

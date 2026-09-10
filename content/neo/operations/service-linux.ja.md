---
toc: true
title: Linuxサービス
type: docs
weight: 82
---

*systemd*または*supervisord*を使用すると、machbase-neoプロセスをシステムサービスとして登録し、起動時に自動的に開始できます。

## 起動・停止スクリプトの作成 {#시작중지-스크립트-작성}

**neo-start.shの作成**

```sh
$ vi neo-start.sh
```

`serve`コマンドに`--pid <path>`フラグを指定して、プロセスIDを指定したパスのファイルに記録します。

```sh {{linenos=table}}
#!/bin/bash
exec /data/machbase-neo serve \
    --pid /data/neo.pid \
    --host 0.0.0.0 \
    --log-filename /data/log/machbase-neo.log
```

シェルスクリプトに実行権限を付与します。

```sh
$ chmod 755 neo-start.sh
```

**neo-stop.shの作成**

```sh
$ vi neo-stop.sh
```

保存したpidファイルを使って`kill`コマンドで停止し、`kill -0`でプロセスが完全に終了するまで待ちます。

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

## systemd {#systemd}

{{% steps %}}

### neo.serviceの作成 {#neoservice-생성}

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

* 環境に合わせて`User`とパスを変更してください。

### サービスの有効化 {#서비스-활성화}

```sh
$ sudo chmod 755 neo.service
$ sudo systemctl daemon-reload
```

ホストの再起動時に自動的に開始するように設定します。

```sh
$ sudo systemctl enable neo.service
```

### 完了 {#완료}

サービスを有効にした後は、以下のコマンドで操作できます。

```sh
$ sudo systemctl start neo.service
$ sudo systemctl status neo.service
$ sudo systemctl stop neo.service
```
{{% /steps %}}

## supervisord {#supervisord}

{{% steps %}}

### neo.confの作成 {#neoconf-생성}

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

* 環境に合わせて`user`とパスを変更してください。
* 上記の例では、ログフォルダー`/data/log`があらかじめ存在する必要があります。

### Supervisordの更新 {#supervisord-업데이트}

```sh
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

### 完了 {#완료-1}

サービスを有効にした後は、次のコマンドでmachbase-neoを操作できます。
```sh
$ sudo supervisorctl start neo
$ sudo supervisorctl status neo
$ sudo supervisorctl stop neo
```

{{% /steps %}}

## PM2 {#pm2}

{{% steps %}}

### neo-start.shの作成 {#neo-startsh-생성}

```sh
$ vi neo-start.sh
```

```sh  {{linenos=table}}
#!/bin/bash
exec /data/machbase-neo serve --host 0.0.0.0
```
* ログはPM2が管理するため、`--log-filename`オプションは不要です。

### neo-start.shへの実行権限の付与 {#neo-startsh-실행-권한-부여}

```sh
$ chmod 755 neo-start.sh
```

### PM2によるmachbase-neoの起動 {#pm2로-machbase-neo-실행}

```sh
$ pm2 start /data/neo-start.sh --name neo --log /data/log/machbase-neo.log
```

machbase-neoの状態を確認します。
```sh
$ pm2 status neo
```

### PM2の自動起動設定 {#pm2-자동-시작-설정}

* 設定済みの場合は、この手順を省略できます。

起動スクリプトを自動生成するには、`pm2 startup`コマンドをsudoなしで実行します。
```sh
$ pm2 startup
[PM2] Init System found: systemd
[PM2] To setup the Startup Script, copy/paste the following command:
sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u machbase --hp /home/machbase
```

表示されたコマンドをコピーしてターミナルに貼り付けます。
```sh  {{linenos=table}}
$ sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u machbase --hp /home/machbase
```
これでPM2は起動時に自動的に再起動します。

### アプリケーション一覧の保存 {#앱-목록-저장}

すべてのアプリケーションを起動した後に一覧を保存すると、再起動後に自動的に復元されます。
```sh
$ pm2 save
```

### 完了 {#완료-2}

以下のコマンドでmachbase-neoを操作できます。

```sh
$ pm2 start neo
$ pm2 status neo
$ pm2 stop neo
$ pm2 restart neo

$ pm2 logs neo
$ pm2 monit
```

{{% /steps %}}

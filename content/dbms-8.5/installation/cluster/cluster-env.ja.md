---
title : 'Cluster Edition のインストール準備'
type: docs
weight: 10
toc: true
---

## オープンファイル数の上限の確認と変更 {#confirm-and-change-file-limit}

オープンできるファイル数の上限を増やすには、次の手順を実行します。

1. /etc/security/limits.conf を編集します。

```bash
sudo vi /etc/security/limits.conf
*       hard   nofile      65535
*       soft   nofile      65535
```

2. 再起動します。

```bash
sudo reboot
# または
sudo shutdown -r now
```

3. 結果を確認します。65535 と表示されれば、変更は成功です。

```bash
ulimit -Sn
```


## サーバー時刻の同期 {#server-time-synchronization}

各ホストの時刻を同期する必要があります。すでに同期済みの場合も、状態を確認してください。

1. すべてのサーバーをタイムサーバーと同期します。

```bash
# 次のコマンドで同期する。
/usr/bin/rdate -s time.bora.net && /sbin/clock -w
```

2. タイムサーバーを利用できない場合は、コマンドで直接設定します。

```bash
# 次のコマンドで変更する。
date -s "2017-10-31 11:15:30"
```

3. 変更後の時刻を確認します。

```bash
# 次のコマンドで確認する。
date
```


## ネットワークのカーネルパラメーターの変更 {#change-network-kernel-parameters}

1. 現在の値を確認します。

```bash
# 次のコマンドで確認する。
sysctl -a | egrep 'mem_(max|default)|tcp_.*mem'
```

2. 次のコマンドで値を変更します（メモリ 64 GB の場合）。

```bash
sudo sysctl -w net.core.rmem_default=33554432     # 32MB
sudo sysctl -w net.core.wmem_default=33554432
sudo sysctl -w net.core.rmem_max=268435456        # 256MB
sudo sysctl -w net.core.wmem_max=268435456
sudo sysctl -w 'net.ipv4.tcp_rmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_wmem=262144 33554432 268435456'
 
# 8388608 Page * 4KB = 32GB
sudo sysctl -w 'net.ipv4.tcp_mem=8388608 8388608 8388608'
```

3. 設定を永続化するには、/etc/sysctl.conf に追加してホスト OS を再起動します。

```bash
# /etc/sysctl.conf を編集する。
net.core.rmem_default = 33554432
net.core.wmem_default = 33554432
net.core.rmem_max     = 268435456
net.core.wmem_max     = 268435456
net.ipv4.tcp_rmem     = 262144 33554432 268435456
net.ipv4.tcp_wmem     = 262144 33554432 268435456
net.ipv4.tcp_mem      = 8388608 8388608 8388608
```

## ユーザーの作成 {#create-user}

1. インストール用の Linux ユーザー machbase を作成します。ホームディレクトリは /home/machbase です。

```bash
$ sudo useradd machbase --home-dir "/home/machbase"
```

2. パスワード（machbase）を設定します。

```bash
sudo passwd machbase
```

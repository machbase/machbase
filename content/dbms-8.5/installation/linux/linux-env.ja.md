---
title : 'Linux 環境の準備'
type : docs
weight: 10
toc: true
---

## オープンファイル数の上限の確認と設定 {#check-and-set-maximum-number-of-files}
1. 次のコマンドで、Linux のオープンファイル数の上限を確認します。
   
```bash
[machbase@localhost ~] ulimit -Sn
1024
```

2. 値が 65535 未満の場合は、次のファイルを変更してサーバーを再起動します。
   
```bash
[machbase@localhost ~] sudo vi /etc/security/limits.conf
 
 
#<domain>      <type>  <item>         <value>
#
 
*               hard    nofile          65535
*               soft    nofile          65535
 
 
[machbase@localhost ~] sudo vi /etc/systemd/user.conf
 
DefaultLimitNOFILE=65535
```

3. 再起動後、値を再確認します。
   
```bash
[machbase@localhost ~] ulimit -Sn
65535
```

## サーバー時刻の確認と設定 {#check-and-set-server-time}

Machbase は時系列データを扱うため、インストール先のサーバー時刻を正しく設定する必要があります。

### タイムゾーンの設定 {#setting-time-zone}

Machbase はサーバーのローカル時刻を使用するため、タイムゾーンの設定がサーバーの時刻と一致していることを確認してください。
次のコマンドで所在地のタイムゾーンと一致するか確認します。異なる場合は、/usr/share/zoneinfo から適切な地域を選び、リンクを設定します。

```bash

[machbase@localhost ~] ls -l /etc/localtime
lrwxrwxrwx 1 root root 32 Sep 27 14:08 /etc/localtime -> ../usr/share/zoneinfo/Asia/Seoul
 
 
# date コマンドで設定済みのタイムゾーンを確認できる。
[machbase@localhost ~] date
Wed Jan  2 11:12:44 KST 2019
```

### 時刻の設定 {#setting-time}

ローカル時刻が正しくない場合は、次のコマンドで設定し直します。

```bash
[machbase@localhost ~] sudo date -s '2018/12/25 12:34:56'
```


## ポートの設定 {#setting-port}

Machbase が使用するポートは、他のプログラムに割り当てられないよう予約します。

次のコマンドで予約すると、OS が他のプログラムにそのポートを割り当てなくなり、競合を防げます。

```bash
[machbase@localhost ~] echo 5656-5657 | sudo tee /proc/sys/net/ipv4/ip_local_reserved_ports
```

上記は一時的な設定です。永続化するには /etc/sysctl.conf を編集します。

```bash
[machbase@localhost ~] sudo vim /etc/sysctl.conf

# Standard の既定のネイティブポートと HTTP REST ポートを予約する。
net.ipv4.ip_local_reserved_ports = 5656-5657
```

Cluster Edition では、設定したクラスタリンク、管理、サービス、
レプリケーション、HTTP のすべてのポートを予約範囲に含めてください。

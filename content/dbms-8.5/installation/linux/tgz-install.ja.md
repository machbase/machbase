---
title : 'tarball によるインストール'
type : docs
weight: 20
toc: true
---

## ユーザーの作成 {#create-user}

インストールと利用のため、Linux ユーザー machbase を作成します。

```bash
sudo useradd machbase
```

パスワードを設定し、machbase アカウントでログインします。


## パッケージのインストール {#package-installation}

`machbase_home` ディレクトリを作成し、Machbase のダウンロードサイトから Standard パッケージを取得して展開します。

```bash
[machbase@localhost ~]$ wget http://machbase.com/dist/machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz
[machbase@localhost ~]$ mkdir machbase_home
[machbase@localhost ~]$ mv machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz machbase_home/
[machbase@localhost ~]$ cd machbase_home/
[machbase@localhost machbase_home]$ tar zxf machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz
 
[machbase@localhost machbase_home]$ ls -l
drwxrwxr-x  5 machbase machbase        64 Oct 30 16:10 3rd-party
drwxrwxr-x  2 machbase machbase      4096 Oct 30 16:10 bin
drwxrwxr-x  2 machbase machbase       306 Jan  2 11:36 conf
drwxrwxr-x  2 machbase machbase       136 Jan  2 11:37 dbs
drwxrwxr-x  3 machbase machbase        22 Oct 30 16:10 doc
drwxrwxr-x  4 machbase machbase        30 Oct 30 16:10 http
drwxrwxr-x  2 machbase machbase        96 Oct 30 16:10 include
drwxrwxr-x  2 machbase machbase        29 Oct 30 16:10 install
drwxrwxr-x  2 machbase machbase       283 Oct 30 16:10 lib
drwxrwxr-x  2 machbase machbase         6 Oct 30 16:10 package
drwxrwxr-x 12 machbase machbase       140 Oct 30 16:10 sample
drwxrwxr-x  2 machbase machbase      4096 Jan  2 09:37 trc
drwxrwxr-x 10 machbase machbase       160 Oct 30 16:10 tutorials
drwxrwxr-x  3 machbase machbase        44 Oct 30 16:10 utility
-rw-rw-r--  1 machbase machbase 139888377 Dec 20 11:33 machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz
 
[machbase@localhost machbase_home]$
```

作成されるディレクトリを示します。

| ディレクトリ | 説明 |
|--|--|
|bin|実行ファイル|
|conf|設定ファイル|
|dbs|データ保存領域|
|doc|ライセンスファイル|
|http|REST API と Web のリソース|
|include|CLI プログラム用のヘッダーファイル|
|install|Makefile 用の mk ファイル|
|lib|ライブラリー|
|package|Cluster Edition で追加したパッケージの保存先|
|sample|サンプルファイル|
|trc|サーバーログとトレース|
|tutorials|チュートリアルファイル|
|utility|ユーティリティーファイル|
|3rd-party|Grafana プラグイン|


## 環境変数の設定 {#set-environment-variable}

.bashrc に Machbase の環境変数を追加します。

```bash

export MACHBASE_HOME=/home/machbase/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
 
# 次のコマンドで変更を反映
source .bashrc
```


## Machbase プロパティの設定 {#set-machbase-property}

`$MACHBASE_HOME/conf` には、標準設定とエディション別のサンプル設定ファイルがあります。

```bash

[machbase@localhost ~]$ cd $MACHBASE_HOME/conf
[machbase@localhost conf]$ ls -l
-rw-rw-r-- 1 machbase machbase 20914 Oct 30 16:10 machbase.conf.sample.standard
-rw-rw-r-- 1 machbase machbase 21363 Oct 30 16:10 machbase.conf.sample.edge
-rw-rw-r-- 1 machbase machbase   407 Oct 30 16:10 machloader.conf.sample
 
[machbase@localhost conf]$
```

Linux の環境変数で接続ポートを変更することもできます。次の例は、既定の 5656 から 7878 に変更します。

```bash
export MACHBASE_PORT_NO=7878
```


## 基本的な操作 {#machbase-simple-usage}

### データベースの作成 {#create-database}

machadmin でデータベースを作成します。--help でコマンドを確認できます。

```bash
[machbase@localhost machbase_home]$ machadmin --help
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
<< available option lists >>
  -u, --startup                         Startup Machbase server.
      --recovery[=simple,complex,reset] Recovery mode. (default: simple)
  -s, --shutdown                        Shutdown Machbase server.
  -c, --createdb                        Create Machbase database.
  -d, --destroydb                       Destroy Machbase database.
  -k, --kill                            Terminate Machbase server.
  -i, --silent                          Produce less output.
  -r, --restore                         Restore Machbase database.
  -x, --extract                         Extract BackupFile to BackupDirectory.
  -w, --viewimage                       Display information of BackupImageFile.
  -e, --check                           Check whether Machbase Server is running.
  -t, --licinstall                      Install the license file.
  -f, --licinfo                         Display information of installed license file.
      --home-path=path                  Specify the home path
 
[machbase@localhost machbase_home]$
```

-c オプションで作成します。

```bash

[machbase@localhost machbase_home]$ machadmin -c
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Database created successfully.
[machbase@localhost machbase_home]$
```

### Machbase サーバーの起動 {#launch-machbase-server}

-u オプションで起動します。

```bash

[machbase@localhost machbase_home]$ machadmin -u
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase server start.
Machbase server started successfully.
[machbase@localhost machbase_home]$
```

次のように ps コマンドで、サーバーデーモン machbased の稼働を確認できます。

```bash
[machbase@localhost machbase_home]$  ps -ef |grep machbased
machbase 11178     1  2 11:25 ?        00:00:01 /home/machbase/machbase_home/bin/machbased -s --recovery=simple
machbase 11276  9867  0 11:26 pts/1    00:00:00 grep --color=auto machbased
[machbase@localhost machbase_home]$
```

### Machbase サーバーへの接続 {#machbase-server-connection}

machsql で接続します。

管理者アカウント SYS が用意されており、パスワードは MANAGER です。

```bash
[machbase@localhost machbase_home]$  machsql
=================================================================
     Machbase Client Query Utility
     Release Version x.x.x.official
     Copyright 2014 MACHBASE Corporation or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1) :
Machbase user ID  (Default:SYS)
Machbase User Password :
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
Type 'help' to display a list of available commands.
Mach>
```

簡単なテーブルを作成し、データを挿入して取得します。

```sql
create table hello( id integer );
insert into hello values( 1 );
insert into hello values( 2 );
select * from hello;
select _arrival_time, * from hello;
```

```sql
Mach> create table hello( id integer );
Created successfully.
Elapsed time: 0.054
Mach> insert into hello values( 1 );
1 row(s) inserted.
Elapsed time: 0.000
Mach> insert into hello values( 2 );
1 row(s) inserted.
Elapsed time: 0.000
Mach> select * from hello;
ID
--------------
2
1
[2] row(s) selected.
Elapsed time: 0.000
Mach> select _arrival_time, * from hello;
_arrival_time                   ID
-----------------------------------------------
2019-01-02 11:33:00 122:806:804 2
2019-01-02 11:32:57 383:848:361 1
[2] row(s) selected.
Elapsed time: 0.000
Mach>
```

SELECT の結果では、最後に入力したデータが先に表示されます。

_arrival_time 列で、入力時刻がナノ秒精度で設定されていることも確認できます。

### Machbase サーバーの停止 {#stop-machbase-server}

-s オプションで停止します。

```bash
[machbase@localhost machbase_home]$ machadmin -s
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase server shut down...
Machbase server shut down successfully.
[machbase@localhost machbase_home]$
```

### データベースの削除 {#delete-database}

-d オプションで削除します。
**すべてのデータが削除されるため、十分に注意してください。**

```bash
[machbase@localhost machbase_home]$ machadmin -d
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.official
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Destroy Machbase database. Are you sure?(y/N) y
Database destroyed successfully.
[machbase@localhost machbase_home]$
```

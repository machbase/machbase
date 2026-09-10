---
title : machadmin
type : docs
weight: 20
toc: true
---

machadmin は、サーバーの起動と停止、データベースの作成と削除、稼働状態の確認に使用します。

## オプションと機能 {#option-and-features}

machadmin のオプションを示します。インストールの節で説明した機能は省略しています。

```bash
mach@localhost:~$ machadmin -h
```

| オプション | 説明 |
|--|--|
|-u, --startup|サーバーを起動|
|--recovery[=simple,complex,reset]|起動時のリカバリーモード（既定値：simple）|
|-s, --shutdown|サーバーを正常終了|
|-c, --createdb|データベースを作成|
|-d, --destroydb|データベースを削除|
|-k, --kill|サーバーを強制終了|
|-i, --silent|出力量を減らす|
|-r, --restore|バックアップから復元|
|-x, --extract|バックアップファイルをバックアップディレクトリへ変換|
|-w, --viewimage|バックアップイメージの情報を表示|
|-e, --check|サーバーの稼働状態を確認|
|-t, --licinstall|ライセンスファイルを導入|
|-f, --licinfo|ライセンス情報を表示|
|--home-path=path|Machbase のホームパスを指定|

## リカバリーモード {#recovery-mode}

構文

```
machadmin -u --recovery=[simple | complex | reset]
```

次のモードがあります。

* simple：稼働中に電源断がなかった場合の既定のモードです。
* complex：simple より時間がかかります。電源断後の再起動時に、既定で実行されます。
* reset：simple と complex で回復できない場合、すべてのテーブルの全データを確認して回復します。一部のデータが失われる場合があります。

## サーバーの正常終了 {#server-normal-shutdown}

例：

```
mach@localhost:~$ machadmin -s
 
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for the server shut down...
Server shut down successfully.
```

## データベースの作成 {#create-database}

例：

```
mach@localhost:~$ machadmin -c
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Database created successfully.
```

## データベースの削除 {#delete-database}

例：

```
mach@localhost:~$ machadmin -d
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Destroy Machbase database- Are you sure?(y/N) y
Database destroyed successfully.
```

## サーバーの強制終了 {#force-to-abort-server}

構文：

```
machadmin -k
```

例：

```
mach@localhost:~$ machadmin -k
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase terminated...
Server terminated successfully.
```

## サイレントモード {#run-silent-mode}

machadmin の実行時に表示するメッセージを抑制します。

構文：

```
machadmin -i
```

## データベースの復元 {#database-recovery}

構文：

```
machadmin -r backup_database_path
```

例：

```
mach@localhost:~$ machadmin -r 'backup'
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Backed up database restored successfully.
```

## サーバーの稼働確認 {#check-server-is-running}

構文：

```
machadmin -e
```


停止中の例：

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
[ERR] Server is not running.
```


稼働中の例：

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Machbase server is already running with PID (14098).
```

## ライセンスファイルの導入 {#install-license-file}

構文：

```
machadmin -t license_file
```


例：

```
mach@localhost:~$ machadmin -t license.dat
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
License installed successfully.
```

## ライセンスの確認 {#check-license}

例：

```
mach@localhost:~$ machadmin -f
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
	                   INFORMATION
ID                                : 00000001
Issue Date                        : 2099-12-31
License Type(Version 3)           : FOGUNLIMITED
Company                           : MACHBASE
Project(Product)                  : NONE
Country Code                      : KR
Install Date                      : 2026-06-13 15:08:00
-----------------------------------------------------------------
License information displayed successfully.
-----------------------------------------------------------------
License information displayed successfully.
```

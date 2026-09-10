---
title : 'machdeployeradmin'
type : docs
weight: 60
toc: true
---

Deployer の状態確認や、起動、終了、強制停止を直接実行するツールです。

通常は machcoordinatoradmin から実行するのが最も簡単ですが、利用できない場合は本ツールを使用します。

Cluster Edition パッケージにのみ含まれます。

## オプションと機能 {#options-and-features}

machdeployeradmin のオプションを示します。前節で説明した機能は省略しています。

```
mach@localhost:~$ machdeployeradmin -h
```


| オプション | 説明 |
|--|--|
| -u, --startup | Deployer プロセスを起動 |
| -s, --shutdown | Deployer プロセスを終了 |
| -k, --kill | Deployer プロセスを強制停止 |
| -c, --createdb | Deployer のメタデータを作成 |
| -d, --destroydb | Deployer のメタデータを削除 |
| -i, --silent | バナーを非表示 |
| -e, --check | Deployer プロセスの稼働状態を確認 |


## 稼働状態の確認 {#checking-running-status}

例：

```
mach@localhost:~$ machdeployeradmin -e
-------------------------------------------------------------------------
     Machbase Deployer Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Machbase Deployer is running with pid(29373)!
```

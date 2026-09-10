---
title : データベースのマウント
type : docs
weight: 30
toc: true
---

* `MOUNT`
* UNMOUNT
* マウントしたデータベースからの読み取り

分析用に大量のデータを継続して保存すると、データ量の増大により次の問題が生じます。

> **エディションに関する注意**：このページは Standard Edition の `MOUNT`/UNMOUNT の動作を説明します。Cluster Edition では `MOUNT` および `UMOUNT` 文が拒否される場合があります。

* 大量のデータ保存によるディスクコストの増加
* 分析用機器のディスク容量の限界

この問題を解決するには、古いデータをバックアップして定期的に削除する必要があります。しかし、後から古いデータを読み取るために復元すると、復元に時間がかかり、データベースのオフライン化も必要になります。サービスを継続するには別の機器が必要です。Machbase は、これらの問題を解決する `MOUNT` コマンドを提供します。

`MOUNT` コマンドは、サービスを継続したままバックアップを読み込み、稼働中のデータベースとは独立したデータベースとして扱います。1 台のサーバーで複数のバックアップを同時に参照できます。ただし、マウントしたデータベースは読み取り専用で、データの追加や削除はできません。

`MOUNT` コマンドにより、バックアップとメインデータベースの内容を同時に読み取れます。マウントしたデータベースも、通常の検索方法で検索できます。

> **注意**：Machbase 8.5 以降では、一般ユーザーが `MOUNT DATABASE` または `UNMOUNT DATABASE` を実行するには、`GRANT MOUNT ON machbasedb TO user_name;` による権限付与が必要です。詳細は[ユーザー管理](../../sql-reference/user-manage/#grantrevoke)の `GRANT/REVOKE` を参照してください。

`MOUNT` の実行には、次の条件を満たす必要があります。
* バックアップデータベースのバージョンとメタデータのバージョンに互換性があること。
* マウントしたバックアップでは、テーブルの作成、インデックスの作成・削除、データの追加・削除はできません。

マウント済みデータベースの情報は、V$STORAGE_MOUNT_DATABASES メタテーブルで確認できます。

## マウント {#mount}

バックアップデータベースのパスと、マウント名を指定します。
バックアップパスには、バックアップコマンドで作成したディレクトリを指定します。マウント名には、稼働中のデータベースと区別できる名前を付けます。
パスには、バックアップコマンドと同様に、`/` で始まる絶対パス、または $MACHBASE_HOME/dbs を基準とする相対パスを指定できます。

構文：

```sql
MOUNT DATABASE 'backup_database_path' TO mount_name;
```

例：

```sql
MOUNT DATABASE '/home/machbase/backup' TO mountdb;
```

## アンマウント {#unmount}

データを読み取る必要がなくなったら、UNMOUNT コマンドでマウントを解除します。

構文：

```sql
UNMOUNT DATABASE mount_name;
```

例：

```sql
UNMOUNT DATABASE mountdb;
```


## マウントしたデータベースからの読み取り {#reading-data-from-mounted-database}

通常と同じ SQL 文でデータを取得します。
マウントしたデータを読み取れるのは SYS ユーザーだけです。SQL 文では、mount_name、user_name、テーブル名を `.` で連結して指定します。

構文：

```sql
SELECT column_name FROM mount_name.user_name.table_name;
```

例：

```sql
SELECT * FROM mountdb.sys.backuptable;
```

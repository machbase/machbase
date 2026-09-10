---
type: docs
title: 'DATABASE'
weight: 220
toc: true
---

Machbase 8.7.0 Standard Editionの論理データベースのライフサイクルとセッション選択の構文です。
データベース名はカタログ名であり、サーバーインスタンスの物理ストレージを管理する`machadmin -c`、`machadmin -d`とは区別します。

## CREATE DATABASE

```sql
create_database_stmt ::=
    'CREATE DATABASE' ['IF NOT EXISTS'] database_name
```

`CREATE DATABASE`は、現在のMachbaseインスタンスにアクティブな論理データベースを作成します。
新しいデータベースのデフォルトのアクセスモードは`READ WRITE`です。
ユーザーと認証情報はインスタンス全体で共有され、テーブル・ビュー・インデックスとオブジェクト権限はデータベースごとに管理されます。

```sql
CREATE DATABASE factory_a;
CREATE DATABASE IF NOT EXISTS factory_b;
```

## ALTER DATABASE

```sql
alter_database_stmt ::=
    'ALTER DATABASE' database_name ( 'READ ONLY' | 'READ WRITE' )
```

`READ ONLY`データベースは検索できますが、書き込みDML、Append、変更DDLは実行できません。
実行中の書き込みを終了してからモードを変更してください。

```sql
ALTER DATABASE factory_a READ ONLY;
ALTER DATABASE factory_a READ WRITE;
```

## DROP DATABASE

```sql
drop_database_stmt ::=
    'DROP DATABASE' ['IF EXISTS'] database_name
    [ 'RESTRICT' | 'CASCADE' | 'FORCE' | 'CASCADE FORCE' | 'FORCE CASCADE' ]
```

- `RESTRICT`は、オブジェクトや使用中の参照がある場合は削除しません。
- `CASCADE`は、対象データベースのオブジェクト、メタデータ、データベースローカルの権限を削除します。
- `FORCE`は、終了可能なセッション、ステートメント、カーソル、ジョブの参照を終了してから削除を進めます。
- オブジェクトと参照を両方削除する場合は、`CASCADE FORCE`を使用します。

デフォルトのデータベース`MACHBASEDB`は削除できません。
現在のセッションのデータベースも削除できないため、先に`USE MACHBASEDB`または別のアクティブなデータベースへのUSEを実行する必要があります。

## USE

```sql
use_database_stmt ::= 'USE' ['DATABASE'] database_name
```

`USE`と`USE DATABASE`は同じ動作です。現在のセッションのデータベースだけを変更し、他の接続には影響しません。
トランザクションの進行中、または対象がマウントされたデータベースの場合は失敗します。

```sql
USE factory_a;
USE DATABASE factory_b;
```

## 現在のデータベースの確認

```sql
SELECT CURRENT_DATABASE();
SELECT DATABASE();
SELECT CURRENT_CATALOG;
SHOW CURRENT DATABASE;
SHOW DATABASES;
```

推奨する確認方法は`CURRENT_DATABASE()`です。
クライアントの接続オプションで初期データベースを指定していても、接続直後にこの値を確認し、実際のサーバーカタログを検証してください。

## オブジェクト名

テーブル・ビューとDMLの対象は、次の形式で指定できます。

```text
table_name                         -- 現在のデータベース、現在のユーザー
owner.table_name                   -- 現在のデータベース、指定した所有者
database_name.owner.table_name    -- 指定したデータベース、指定した所有者
```

2部構成の名前は常に`owner.table`です。
したがって、`factory_a.sensor_log`はデータベースとテーブルの2部構成の名前とは解釈されません。
別のデータベースを明示するには、`factory_a.sys.sensor_log`のように3部構成を使用します。

```sql
SELECT * FROM factory_a.sys.sensor_log;
INSERT INTO factory_b.app.orders VALUES (1, 'ready');
```

別のデータベースを直接参照するには、対象データベースの`CONNECT`と対象テーブルの必要なDML権限が両方必要です。
インデックス名、`LOAD DATA`の対象などは、各構文の修飾子の制約に従います。

## 権限構文とデータベース範囲

データベース権限とテーブル権限は別です。基本形式は次のとおりです。

```sql
GRANT CONNECT ON DATABASE factory_a TO app_a;
GRANT CREATE, ALTER ON DATABASE factory_a TO deployer;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_a;
REVOKE CONNECT ON DATABASE factory_a FROM app_a;
```

マウントされたデータベースを検索するには、対象データベースの`USAGE`とテーブルの`SELECT`が両方必要です。
`MOUNT DATABASE`と`UMOUNT DATABASE`を実行する運用権限は、[USER/AUTH構文](../user-auth-syntax/#grant-revoke)と
[複数データベースの運用ガイド](/dbms/operations-configuration-recovery/multi-database/)を参照してください。

## BACKUP/RESTOREとの関係

論理データベースのバックアップ・リストア構文は、[BACKUP / RESTORE / MOUNT](../backup-restore-mount-syntax/)にまとめています。
単一のアクティブカタログを対象とした名前付きバックアップだけを、論理MOUNTまたはRESTOREの入力に使用できます。
複数のアクティブデータベースを含むインスタンス全体のイメージは、論理カタログとしてマウント・リストアできません。

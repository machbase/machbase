---
type: docs
title: '14.3 権限管理'
weight: 30
toc: true
---

Machbase の権限は、アクティブデータベース単位の管理権限と、特定テーブルの DML 権限に分かれます。
ユーザーにはデータベース接続用の `CONNECT` と、実際の操作対象に必要な権限の両方が必要です。

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

<a id="privileges"></a>

## 権限モデル

| 範囲 | 権限 | 用途 |
|---|---|---|
| アクティブデータベース | `CONNECT` | 接続と `USE` |
| アクティブデータベース | `CREATE`, `DROP`, `ALTER` | オブジェクトの作成・削除・変更 |
| アクティブデータベース | `BACKUP` | データベースのバックアップ |
| アクティブデータベース | `DDL` | `CREATE` と `DROP` の組み合わせ |
| アクティブデータベース | `ALL` | `CONNECT`, `CREATE`, `DROP`, `ALTER`, `BACKUP` |
| マウントされたデータベース | `USAGE` | マウント内の参照 |
| 管理データベース | `MOUNT` | `MOUNT DATABASE`, `UMOUNT DATABASE` |
| テーブル | `SELECT`, `INSERT`, `DELETE`, `UPDATE` | 特定テーブルの DML |
| テーブル | `ALL` | 4種類のテーブル DML 権限 |

データベースの `ALL` にテーブル DML や `MOUNT` は含まれません。テーブルの `ALL` にも
データベース管理権限は含まれません。権限があっても、テーブルタイプが非対応の DML は実行できません。
例えば LOG は `UPDATE` をサポートしません。

<a id="grant-revoke"></a>

## GRANT / REVOKE

```sql
GRANT privilege_list ON target TO user_name;
REVOKE privilege_list ON target FROM user_name;
```

次の例は、ユーザーにデータベース接続と1テーブルの読み書きを許可します。

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;

REVOKE INSERT ON TABLE factory_a.sys.sensor_log FROM app_user;
REVOKE CONNECT ON DATABASE factory_a FROM app_user;
```

テーブルは現在のデータベースの `owner.table` または `database.owner.table` で指定できます。
データベース全体に `SELECT` などの DML 権限を付与する構文はサポートされません。

現在の権限記録は `M$SYS_USER_ACCESS` で確認します。

```sql
SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY DB_NAME, OWNER_NAME, TABLE_NAME;
```

`OWNER_NAME` と `TABLE_NAME` が `NULL` ならデータベース単位、値があればテーブル単位の記録です。
`PRIV` は複数権限を表すビットマスクです。表示された数値を単独の権限名と解釈したり、
運用スクリプトに固定したりしないでください。

<a id="database-privileges"></a>

## データベース権限

ユーザーを作るだけでは論理データベースに接続できません。対象データベースの `CONNECT` を明示的に
付与し、必要な管理権限を最小単位で追加します。

```sql
GRANT CONNECT ON DATABASE factory_a TO deploy_user;
GRANT DDL ON DATABASE factory_a TO deploy_user;
GRANT ALTER ON DATABASE factory_a TO deploy_user;
```

新規ユーザーに記録されるデフォルトの互換権限は、デフォルトデータベース `MACHBASEDB` の範囲です。
他の論理データベースへ自動的には拡張されません。

<a id="select-insert-delete-update"></a>
<a id="database-privileges-select-insert-delete-update"></a>

### SELECT / INSERT / DELETE / UPDATE

DML 権限は特定テーブルに対して付与します。

```sql
GRANT SELECT ON sys.sensor_log TO reader_user;
GRANT INSERT ON sys.sensor_log TO writer_user;
GRANT DELETE ON sys.device_config TO maint_user;
GRANT UPDATE ON sys.device_config TO maint_user;
```

`DELETE` と `UPDATE` の付与前に、対象タイプの条件制約も確認します。TAG の変更にはタグと時間条件、
VOLATILE の変更には主キー条件が必要です。

<a id="create-drop"></a>
<a id="database-privileges-create-drop"></a>

### CREATE / DROP

```sql
GRANT CREATE ON DATABASE factory_a TO deploy_user;
GRANT DROP ON DATABASE factory_a TO deploy_user;
```

`DROP` は復旧が難しい変更を許可するため、ロード・検索専用アカウントには付与しないでください。
オブジェクト所有権だけでは、他のデータベースへ接続できません。

<a id="database-privileges-alter"></a>

### ALTER

```sql
GRANT ALTER ON DATABASE factory_a TO deploy_user;
```

`ALTER` はテーブル構造と運用設定の変更に影響します。アプリケーションとは別のデプロイ・運用アカウントに
だけ付与し、変更後に現在の設定とスキーマを再取得してください。

<a id="database-privileges-backup"></a>

### BACKUP

```sql
GRANT BACKUP ON DATABASE factory_a TO backup_user;
```

SQL 権限とは別に、サーバープロセスの OS アカウントにはバックアップパスへの書き込み権限と空き容量が
必要です。バックアップ用ユーザーに DML・DDL 権限を併せて付与しない構成を推奨します。

<a id="database-privileges-mount"></a>

### MOUNT

```sql
GRANT MOUNT ON DATABASE MACHBASEDB TO recovery_user;
```

MOUNT/UMOUNT は管理操作です。マウントされたデータベースを参照する `USAGE` と、そのテーブルを読む
`SELECT` は別の権限です。実際の復旧は
[バックアップ・リストア・マウント](/dbms/operations-configuration-recovery/backup-restore-mount/)に従ってください。

<a id="privileges-ddl-all"></a>
<a id="database-privileges-privileges-ddl-all"></a>

### DDL / ALL の複合権限

```sql
-- CREATE + DROP
GRANT DDL ON DATABASE factory_a TO deploy_user;

-- アクティブデータベースの CONNECT, CREATE, DROP, ALTER, BACKUP
GRANT ALL ON DATABASE factory_a TO database_admin;

-- 1つのテーブルの SELECT, INSERT, DELETE, UPDATE
GRANT ALL ON TABLE factory_a.sys.sensor_log TO table_admin;
```

複合権限は便利ですが、最小権限の確認を難しくする場合があります。自動化アカウントには、
可能な限り個別の権限を付与してください。

<a id="privileges-grant-exclude"></a>

## デフォルト権限と対象外の権限

`CREATE USER` で作ったユーザーには、`MACHBASEDB` のデフォルト互換権限が記録されます。
論理データベースでは、次のように必要な範囲を明示する構成を基本にします。

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

`ALTER`、`BACKUP`、`MOUNT`、`USAGE` と他の論理データベースの権限は、業務上の役割を確認して
別途付与します。

<a id="privileges-2"></a>

## テーブル権限

テーブル権限は必ず対象オブジェクトとともに管理します。

```sql
GRANT SELECT ON TABLE factory_a.sys.sensor_log TO reader_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO ingest_user;

REVOKE INSERT ON TABLE factory_a.sys.sensor_log FROM ingest_user;
```

テーブルを削除すると既存の grant も削除され、同名の新オブジェクトには引き継がれません。
必要な権限を再付与し、`M$SYS_USER_ACCESS` で確認してください。

<a id="checklist-diagnosis-privileges"></a>

## 権限診断チェックリスト

ユーザーと権限を次の順序で確認します。

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;

SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 ORDER BY USER_NAME, DB_NAME, OWNER_NAME, TABLE_NAME;
```

- 未使用アカウントが残っていないか確認します。
- 読み取り用アカウントに書き込み・DDL・管理権限がないか確認します。
- 承認期間が終了した一時権限を `REVOKE` し、結果を再取得します。
- ユーザー削除前に所有オブジェクトと実行中のセッションを確認します。
- `PRIV` を数値から解釈する監査ツールは、稼働バージョンの権限定義と併せて検証します。

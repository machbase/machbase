---
type: docs
title: 'BACKUP / RESTORE / MOUNT'
weight: 170
toc: true
---

Machbaseのバックアップ・リストア・マウント構文は、データを保護し、必要に応じて復旧や過去データの検索を行うために使用します。

> **権限**: 一般ユーザーがバックアップ・マウントを実行するには、別の権限が必要です。
> ```sql
> GRANT BACKUP ON DATABASE database_name TO user_name;
> GRANT MOUNT  ON DATABASE MACHBASEDB TO user_name;
> ```

---

## BACKUP

### 論理データベースのバックアップ

8.7.0 Standard Editionでは、対象カタログを明示する論理バックアップを使用できます。

```sql
backup_logical_database_stmt ::=
    'BACKUP DATABASE' database_name
    [ 'AFTER' 'backup_path_or_lsn' ]
    'INTO DISK' '=' 'backup_path'
```

```sql
BACKUP DATABASE factory_a INTO DISK = '/backup/factory_a_20260806';
BACKUP DATABASE factory_a AFTER '/backup/factory_a_20260806'
  INTO DISK = '/backup/factory_a_inc';
```

論理バックアップは、1つのアクティブなデータベースカタログを対象とします。
複数のアクティブデータベースを含むインスタンス全体のイメージは、論理`MOUNT`または`RESTORE`の入力には使用できません。

### フルバックアップ

```sql
backup_database_stmt ::=
    'BACKUP DATABASE INTO DISK' '=' 'backup_path'
    [ 'IMPORT MODE' ]
```

現在のデータベース全体を指定パスに保存します。サーバーを停止せずに実行するオンラインバックアップです。

```sql
-- 絶対パスでフルバックアップ
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';

-- 相対パス（$MACHBASE_HOME/dbs基準）
BACKUP DATABASE INTO DISK = 'backup_20240101';
```

- `backup_path`がすでに存在するとエラーになります。日付などを含む一意の名前を使用してください。
- バックアップ完了まで、コマンドはブロックします。

### 増分バックアップ

```sql
backup_incremental_stmt ::=
    'BACKUP DATABASE AFTER' 'backup_path_or_lsn'
    'INTO DISK' '=' 'backup_path'
```

最後のフルバックアップまたは増分バックアップを基準にバックアップします。
テーブルタイプごとの保存方式は区別する必要があります。
TRANSACTIONストレージは増分イメージにもその時点の全体スナップショットとして含まれるため、変更行だけの差分や変更量に相当する容量として計算しないでください。
[TRANSACTIONのバックアップ検証](/dbms/rdb-table-usage/backup-restore-mount/)で、バックアップと現在のデータの検索を比較できます。

```sql
-- フルバックアップ後の変更の増分バックアップ
BACKUP DATABASE AFTER '/backup/machbase_20240101'
INTO DISK = '/backup/incr_20240102';
```

### 期間バックアップ

```sql
backup_period_stmt ::=
    'BACKUP DATABASE'
    'FROM' datetime_expr 'TO' datetime_expr
    'INTO DISK' '=' 'backup_path'
```

指定した時間範囲に該当するデータだけをバックアップします。

```sql
BACKUP DATABASE
FROM TO_DATE('2024-01-01','YYYY-MM-DD')
TO   TO_DATE('2024-02-01','YYYY-MM-DD')
INTO DISK = '/backup/period_jan';
```

### テーブルのバックアップ

```sql
backup_table_stmt ::=
    'BACKUP TABLE' table_name 'INTO DISK' '=' 'backup_path'
```

データベース全体ではなく、特定のテーブルだけを選択してバックアップします。

```sql
BACKUP TABLE sensor_log INTO DISK = '/backup/sensor_log_20240101';
```

---

## RESTORE

従来の`machadmin -r`は、サーバーを停止するオフラインのインスタンス復旧です。
8.7.0 Standard Editionでは、論理データベースを新しいカタログに復元するか、READ ONLYの対象を置換する、
オンラインの`RESTORE DATABASE`もサポートします。

```sql
restore_database_stmt ::=
    'RESTORE DATABASE' database_name 'FROM DISK' '=' 'backup_path'
    [ 'REMAP OWNER' old_owner 'TO' new_owner ]
    [ 'REPLACE' ]
```

```sql
RESTORE DATABASE factory_a_copy
  FROM DISK = '/backup/factory_a_20260806'
  REMAP OWNER APP_A TO APP_ARCHIVE;

RESTORE DATABASE factory_a
  FROM DISK = '/backup/factory_a_20260806'
  REPLACE;
```

`RESTORE DATABASE`はSYS専用です。
`REPLACE`の対象はREAD ONLYで参照がないことが必要です。
リストア後にデータベース・テーブル権限は自動継承されないため、再付与する必要があります。
バックアップイメージの未サポートオブジェクトや所有者の競合によって、リストア全体が失敗する場合があります。

### 既存インスタンスのオフライン復旧（`machadmin -r`）

復旧前にバックアップSQLファイルを準備・検証してから実行します。

```sql
-- /secure/path/pre_restore_backup.sql
BACKUP DATABASE INTO DISK = '/backup/before_restore';
```

```bash
# 1. 復旧前に現在のデータをバックアップ
machsql -s 127.0.0.1 -P 5656 -u SYS \
  -f /secure/path/pre_restore_backup.sql

# 2. サーバー終了
machadmin -s

# 3. 現在のデータベースを削除
machadmin -d

# 4. バックアップデータから復元
machadmin -r /backup/machbase_20240101

# 5. サーバー起動
machadmin -u
```

`machadmin -d`は現在のデータベースを破棄します。
復旧対象、バックアップ、元に戻す計画を確認し、明示的な承認を得た後だけ実行してください。
リストアすると、現在のデータベースはバックアップ時点の状態に完全に置き換わります。

### 増分バックアップのリストア

復元する最後の増分バックアップのパスを一度指定します。
増分バックアップはチェーン情報を含むため、フルバックアップから繰り返し適用する必要はありません。

```bash
machadmin -s
machadmin -d
machadmin -r /backup/incr_20240103
machadmin -u
```

### machadminの主なオプション

| オプション | 説明 |
|------|------|
| `-s` (`--shutdown`) | サーバーの正常終了 |
| `-k` (`--kill`) | サーバーの強制終了 |
| `-u` (`--startup`) | サーバーの起動 |
| `-d` (`--destroydb`) | 現在のデータベースの削除 |
| `-r path` (`--restore`) | 指定したバックアップパスから復元 |

---

## MOUNT DATABASE

```sql
mount_database_stmt ::=
    'MOUNT DATABASE' 'backup_database_path' 'TO' mount_name
```

サーバーを停止したりアクティブなデータベースを置換したりせずに、単一カタログのバックアップイメージを現在のサーバーへマウントデータベースとして接続します。
マウントデータベースは常にREAD ONLYであり、`USE`で現在のデータベースにはできません。

- `backup_database_path`: DISK方式で作成したバックアップディレクトリのパス
- `mount_name`: マウントデータベースへのアクセスに使用するデータベース別名

```sql
-- 絶対パスでマウント
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 相対パス（$MACHBASE_HOME/dbs基準）
MOUNT DATABASE 'machbase_20240101' TO backup_db;
```

### マウントしたデータベースの検索

マウントしたデータベースのテーブルには、`mount_name.user_name.table_name`形式でアクセスします。
検索には、マウントデータベースの`USAGE`と対象テーブルの`SELECT`が両方必要です。

```sql
-- マウントしたデータベースのテーブルを検索
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-01','YYYY-MM-DD');

-- 現在のデータベースとマウントデータベースを結合して検索（JOIN）
SELECT a.name, a.value AS current_val, b.value AS backup_val
  FROM sensor_log a
  JOIN backup_db.sys.sensor_log b ON a.name = b.name;
```

---

## UMOUNT DATABASE

```sql
umount_database_stmt ::=
    'UMOUNT DATABASE' mount_name
```

マウントしたデータベースを解除します。

```sql
UMOUNT DATABASE backup_db;
```

マウントデータベースを参照する開いたカーソルや実行中のクエリがある場合、アンマウントは失敗します。
該当するセッションを終了してから再実行してください。

---

## 制約と注意事項

| 項目 | 説明 |
|------|------|
| マウントデータベースへの書き込み | 不可（読み取り専用） |
| IBFILE方式バックアップのマウント | 不可（DISK方式だけマウント可能） |
| バージョン互換性 | バックアップデータベースと現在のサーバーのメタバージョンに互換性が必要 |
| TAGテーブルの期間復元 | 未サポート（フルバックアップまたは増分バックアップからのみ復元可能） |
| Cluster Edition | 複数データベースとMOUNT/UMOUNTは未サポート |

---

## 関連文書

- [バックアップ・リストア・マウント運用ガイド](/dbms/operations-configuration-recovery/backup-restore-mount/) - 詳細な運用手順と自動化例
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) - バックアップ・マウント権限の付与

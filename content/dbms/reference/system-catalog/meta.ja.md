---
type: docs
title: '16.3.1 メタデータテーブル辞典'
weight: 10
toc: true
---

メタデータテーブルは`M$`で始まり、テーブル定義、列、インデックス、ユーザーなどのMachbaseスキーマ情報を参照します。DDLの実行結果を自動反映する読み取り専用テーブルです。

8.7.0 Standard Editionの複数データベース環境でカタログローカルなメタデータを結合するときは、
`DATABASE_ID`、`TABLESPACE_ID`、親オブジェクトIDを併用してください。論理的な`DATABASE_ID`と
物理的な`TABLESPACE_ID`は相互に代用できません。データベースの運用境界は
[複数データベースの運用ガイド](/dbms/operations-configuration-recovery/multi-database/)を参照してください。

## メタデータテーブル一覧

| テーブル名 | 説明 |
|------------|------|
| `M$SYS_TABLES` | ユーザー作成テーブルの一覧とタイプ |
| `M$SYS_TABLE_PROPERTY` | テーブルに適用されたプロパティ情報 |
| `M$SYS_COLUMNS` | テーブルの列定義（型、長さなど） |
| `M$SYS_INDEXES` | インデックス定義 |
| `M$SYS_INDEX_COLUMNS` | インデックスを構成する列の情報 |
| `M$SYS_TABLESPACES` | テーブルスペース一覧 |
| `M$SYS_TABLESPACE_DISKS` | テーブルスペースが使用するディスクパス |
| `M$SYS_USERS` | 登録済みユーザー一覧 |
| `M$SYS_VIEWS` | ビューを定義するSQLテキスト |
| `M$SYS_USER_ACCESS` | テーブル別のユーザー権限 |
| `M$RETENTION` | 保持ポリシー情報 |
| `M$TABLES` | M$メタデータテーブル自体の一覧 |
| `M$COLUMNS` | M$メタデータテーブルの列一覧 |

## M$SYS_TABLES

ユーザーが作成したテーブルの一覧とタイプを参照します。

| 列名 | 型 | 説明 |
|--------|------|------|
| `NAME` | VARCHAR | テーブル名 |
| `TYPE` | INTEGER | テーブルタイプ |
| `ID` | LONG | テーブル識別子 |
| `DATABASE_ID` | LONG | 論理データベース識別子 |
| `TABLESPACE_ID` | LONG | 物理テーブルスペース識別子 |
| `USER_ID` | INTEGER | テーブルを作成したユーザーの識別子 |
| `COLCOUNT` | INTEGER | 列数 |
| `FLAG` | INTEGER | サブタイプ（1: Tag Data, 2: Rollup, 4: Tag Meta, 8: Tag Stat） |

**TYPE値の意味:**

| 値 | テーブルタイプ |
|----|------------|
| `0` | Log テーブル |
| `1` | Fixed テーブル |
| `3` | Volatile テーブル |
| `4` | Lookup テーブル |
| `5` | Key Value テーブル |
| `6` | Tag テーブル |
| `7` | View |
| `8` | TRANSACTION テーブル |

## M$SYS_COLUMNS

テーブルの列定義を参照します。

| 列名 | 型 | 説明 |
|--------|------|------|
| `NAME` | VARCHAR | 列名 |
| `TYPE` | INTEGER | 列のデータ型 |
| `TABLE_ID` | LONG | 所属テーブルの識別子 |
| `DATABASE_ID` | LONG | 論理データベース識別子 |
| `TABLESPACE_ID` | LONG | 物理テーブルスペース識別子 |
| `LENGTH` | INTEGER | 列の最大長 |
| `PART_PAGE_COUNT` | INTEGER | パーティション当たりのページ数 |
| `MINMAX_CACHE_SIZE` | LONG | MIN-MAXキャッシュサイズ |

## M$SYS_INDEXES

インデックス定義を参照します。

| 列名 | 型 | 説明 |
|--------|------|------|
| `NAME` | VARCHAR | インデックス名 |
| `TYPE` | INTEGER | インデックスタイプ |
| `TABLE_ID` | LONG | 所属テーブルの識別子 |
| `DATABASE_ID` | LONG | 論理データベース識別子 |
| `TABLESPACE_ID` | LONG | 物理テーブルスペース識別子 |
| `COLCOUNT` | INTEGER | インデックスの列数 |
| `MAX_LEVEL` | INTEGER | 最大LSMレベル |

## M$SYS_USERS

登録済みユーザー一覧を参照します。

| 列名 | 型 | 説明 |
|--------|------|------|
| `USER_ID` | INTEGER | ユーザー識別子 |
| `NAME` | VARCHAR | ユーザー名 |
| `PWD_POLICY_LEVEL` | INTEGER | パスワードポリシーレベル |
| `VALID_BEFORE` | VARCHAR | アカウントの有効期間 |

## M$RETENTION

保持ポリシーの情報を参照します。

| 列名 | 型 | 説明 |
|--------|------|------|
| `POLICY_NAME` | VARCHAR | ポリシー名 |
| `DURATION` | LONG | 保持期間（秒） |
| `INTERVAL` | LONG | 削除実行間隔（秒） |

## SQL例

```sql
-- 全テーブル一覧（タイプを含む）
SELECT name, type, colcount
  FROM m$sys_tables
 ORDER BY name;

-- Tagテーブルのみ参照（type = 6）
SELECT name FROM m$sys_tables WHERE type = 6;

-- 特定テーブルの列一覧
SELECT c.name AS col_name, c.type AS col_type, c.length
  FROM m$sys_columns c
  JOIN m$sys_tables  t
    ON c.database_id = t.database_id
   AND c.tablespace_id = t.tablespace_id
   AND c.table_id = t.id
 WHERE t.name = 'SENSOR_TAG'
 ORDER BY c.id;

-- 特定テーブルのインデックス一覧
SELECT i.name AS idx_name, i.type AS idx_type, i.colcount
  FROM m$sys_indexes i
  JOIN m$sys_tables  t
    ON i.database_id = t.database_id
   AND i.tablespace_id = t.tablespace_id
   AND i.table_id = t.id
 WHERE t.name = 'SENSOR_TAG';

-- インデックスを構成する列の確認
SELECT ic.name AS col_name, ic.index_type
  FROM m$sys_index_columns ic
  JOIN m$sys_indexes i ON ic.index_id = i.id
  JOIN m$sys_tables  t ON i.table_id = t.id
 WHERE t.name = 'SENSOR_TAG';

-- テーブルスペースのディスクパスの確認
SELECT ts.name AS tbs_name, d.path, d.io_thread_count
  FROM m$sys_tablespace_disks d
  JOIN m$sys_tablespaces ts ON d.tablespace_id = ts.id;

-- ユーザー一覧の参照
SELECT user_id, name, pwd_policy_level, valid_before
  FROM m$sys_users;

-- 保持ポリシー一覧
SELECT * FROM m$retention;
```

> メタデータテーブルは読み取り専用です。`INSERT`、`UPDATE`、`DELETE`はエラーを返します。スキーマの変更には`CREATE TABLE`、`ALTER TABLE`、`DROP TABLE`などのDDLを使用してください。

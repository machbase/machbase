---
type: docs
title: '16.3.4 V$STORAGE_MOUNT_DATABASES辞典'
weight: 50
toc: true
---

`V$STORAGE_MOUNT_DATABASES`は、現在のインスタンスに読み取り専用で接続したバックアップデータベースを表示します。

## 列

| 列 | 型 | 説明 |
|---|---|---|
| `NAME` | VARCHAR | バックアップデータベース名 |
| `PATH` | VARCHAR | バックアップイメージの元のパス |
| `BACKUP_TBSID` | LONG | バックアップのテーブルスペース識別子 |
| `BACKUP_SCN` | LONG | バックアップSCN |
| `MOUNTDB` | VARCHAR | MOUNT時に指定したデータベースのエイリアス |
| `DB_BEGIN_TIME` | VARCHAR | バックアップデータの開始時刻 |
| `DB_END_TIME` | VARCHAR | バックアップデータの終了時刻 |
| `BACKUP_BEGIN_TIME` | VARCHAR | バックアップ処理の開始時刻 |
| `BACKUP_END_TIME` | VARCHAR | バックアップ処理の終了時刻 |
| `FLAG` | INTEGER | 内部状態フラグ。値の意味を推測しないこと |

## 参照

```sql
SELECT NAME, PATH, MOUNTDB,
       DB_BEGIN_TIME, DB_END_TIME,
       BACKUP_BEGIN_TIME, BACKUP_END_TIME
  FROM V$STORAGE_MOUNT_DATABASES
 ORDER BY MOUNTDB;
```

## MOUNTと参照の例

```sql
MOUNT DATABASE '/data/backup/sc15_snapshot' TO backup_check;

SELECT *
  FROM backup_check.sys.target_table
 LIMIT 10;

UMOUNT DATABASE backup_check;
```

オペランドはバックアップパス、`TO`、エイリアスの順です。マウント済みデータベースのオブジェクトは
`mount_alias.owner.table`という3部構成の名前で参照します。権限と安全上の制約の全体は
[BACKUP/RESTORE/MOUNT構文](/dbms/reference/sql/syntax/backup-restore-mount-syntax/)を参照してください。

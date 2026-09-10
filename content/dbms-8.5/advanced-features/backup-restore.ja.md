---
title : バックアップと復元
type : docs
weight: 20
toc: true
---

## データベースのバックアップ {#database-backup}

> **注意**：Machbase 8.5 以降では、一般ユーザーが `BACKUP DATABASE` を実行するには、`GRANT BACKUP ON machbasedb TO user_name;` による権限付与が必要です。詳細は[ユーザー管理](../../sql-reference/user-manage/#grantrevoke)の `GRANT/REVOKE` を参照してください。

Machbase のバックアップには次の種類があり、データベース全体または特定のテーブルを対象にできます。
  - フルバックアップ：すべてのデータをバックアップ
  - 増分バックアップ：フルバックアップまたは前回の増分バックアップ以降に追加されたデータをバックアップ
  - 期間指定バックアップ：指定期間のデータをバックアップ

構文：

```sql
# フルバックアップ
BACKUP [ DATABASE | TABLE table_name ]  INTO [ DISK ] = 'path/backup_name';
time_duration = FROM start_time TO end_time

# 増分バックアップ
BACKUP [ DATABASE | TABLE table_name ] AFTER 'previous_backup_dir' INTO [ DISK ] = 'path/backup_name';

# 期間指定バックアップ
BACKUP [ DATABASE | TABLE table_name ]  [ time_duration ] INTO [ DISK ] = 'path/backup_name';
```
パスには絶対パスと相対パスを指定できます。
`time_duration` には、対象データの開始時刻と終了時刻を指定します。

例：

```sql
-- フルバックアップ
BACKUP DATABASE INTO DISK = 'backup_dir_name';

-- 増分バックアップ
BACKUP DATABASE AFTER 'previous_backup_dir' INTO DISK = 'path/backup_name';

-- 期間指定バックアップ
BACKUP DATABASE FROM TO_DATE('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS')
                TO TO_DATE('2015-07-14 23:59:59','YYYY-MM-DD HH24:MI:SS')
                INTO DISK = '/home/machbase/backup_20150714'
```

バックアップの種類と保存先パスを指定します。データベース全体を対象にする場合は DATABASE、特定のテーブルを対象にする場合は TABLE とテーブル名を指定します。

`time_duration` 句で対象期間を指定できます。FROM に開始時刻、TO に終了時刻を指定します。上の例では FROM が `2015-07-14 00:00:00`、TO が `2015-07-14 23:59:59` で、2015 年 7 月 14 日のデータを対象とします。期間を省略すると、FROM は `1970-01-01 00:00:00`、TO は実行時の現在時刻になります。

相対パスを指定すると、バックアップは `$MACHBASE_HOME/dbs` の下に作成されます。絶対パスは `/` で始めてください。


## データベースの復元 {#database-restore}

バックアップから復元する際には、次の制約があります。
* クエリーでは実行できません。machadmin コマンドを使用します。
* データベースを停止する必要があります。
* 復元により現在のデータは削除されます。現在のデータが不要であることを確認してください。
* 増分バックアップの復元には、それ以前のフルバックアップと増分バックアップが必要です。
* Tag テーブルでは、期間指定バックアップの復元はサポートされません。

構文：

```bash
machadmin -r backup_database_path
```

例：

```bash
backup database into disk = '/home/machbase/backup';

machadmin -k
machadmin -d
machadmin -r /home/machbase/backup;
```

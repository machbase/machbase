---
title : バックアップの概要
type : docs
weight: 10
toc: true
---

## `BACKUP`/`MOUNT` の概念 {#the-concept-of-backupmount}

> **エディションに関する注意**：本ページは Standard Edition のバックアップとマウントを説明します。Cluster Edition では、`BACKUP`、`MOUNT`、`UMOUNT` 文が拒否される場合があります。

データベースの永続性を保つため、メモリ上のデータはできるだけ早くディスクに保存されます。プロセス障害などは再起動時のリカバリーで整合性を回復できますが、停電や火災によるハードウェア損傷では復旧できない場合があります。バックアップと復元は、データを別の場所のディスクや機器に定期保存し、緊急時にそのデータから復旧する機能です。

バックアップは実行時の状態により、次の 2 種類に分かれます。
* オフラインバックアップ
* オンラインバックアップ

オフラインバックアップは、DBMS を停止してデータベースをコピーする方法で、コールドバックアップとも呼びます。手順は簡単ですが、サービスが中断します。そのため、運用中よりも初期テストやデータ構築時に使用します。

オンラインバックアップは、DBMS の稼働中に実行する方法で、ホットバックアップとも呼びます。サービスを中断せずに実行でき、可用性を維持できます。通常、DBMS のバックアップはこの方式を指します。Machbase は時系列データベースとして期間指定バックアップも提供し、指定した時刻範囲のデータだけをバックアップできます。

![overview1](/dbms-8.5/advanced-features/overview1.png)

```sql
backup database into disk = 'backup';
backup database from to_date('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS') to to_date('2015-07-14 23:59:59 999:999:999','YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn')
                into disk = 'backup_20150714';
```

バックアップしたデータベースは、復元（Restore）によって再利用できます。復元では、破損したデータベースを削除し、バックアップイメージからプライマリーデータベースを再作成します。既存データベースを削除してから machadmin -r を実行してください。

```bash
machadmin -r 'backup'
```

マウントとアンマウントは、バックアップを稼働中のデータベースに接続、または接続解除するオンライン機能です。

```sql
mount database 'backup' to mountName;
umount database mountName;
```

## データベースのバックアップ {#database-backup}

Machbase は、稼働中のデータベース全体を対象とする DATABASE バックアップと、必要なテーブルだけを対象とする TABLE バックアップを提供します。
次のバックアップコマンドを使用します。

```bash
BACKUP [ DATABASE | TABLE table_name ]  [ time_duration ] INTO DISK = 'path/backup_name';
time_duration = FROM start_time TO end_time
path = 'absolute_path' or  'relative_path'
```

```
-- ディレクトリへのバックアップ
BACKUP DATABASE INTO DISK = 'backup_dir_name';

-- 期間指定バックアップ
BACKUP DATABASE FROM TO_DATE('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS')
                     TO TO_DATE('2015-07-14 23:59:59','YYYY-MM-DD HH24:MI:SS')
                     INTO DISK = '/home/machbase/backup_20150714'
```

バックアップの種類、対象期間、保存先パスを指定します。全体を対象にする場合は DATABASE、特定のテーブルを対象にする場合は TABLE とテーブル名を指定します。`time_duration` 句の FROM に開始時刻、TO に終了時刻を指定すると、その期間だけを対象にできます。2 番目の SQL 例では、`2015-07-14 00:00:00` から `2015-07-14 23:59:59` まで、7 月 14 日のデータを対象にします。期間を省略すると、FROM は `1970-01-01 09:00:00`、TO はコマンドの実行時刻になります。


保存媒体を指定します。単一ファイルとして作成する場合は IBFILE、ディレクトリ単位で作成する場合は DISK を指定します。保存先の PATH が相対パスの場合、現在の DB 設定の DB_PATH 配下に作成されます。別の場所に保存するには、`/` で始まる絶対パスを指定します。


### 増分バックアップ {#incremental-backup}

増分バックアップは、前回のバックアップ後に入力されたデータだけを保存します。対象は Log テーブルと Tag テーブルです。Lookup テーブルは常に全データをバックアップします。
実行には、前回の増分バックアップまたはフルバックアップのディレクトリが必要です。
次のように実行します。

```sql
Mach> BACKUP DATABASE INTO DISK = 'backup1'; /* フルバックアップを実行 */
Executed successfully.
Mach> ...
  
Mach> BACKUP DATABASE AFTER 'backup1' INTO DISK = 'backup2'; /* backup1 以降に入力したデータを増分バックアップ */
Executed successfully.
Mach> ...
```

増分バックアップは、データベース全体、Log テーブル、Tag テーブルで使用できます。データベース全体の場合、Lookup テーブルはフルバックアップになります。復元には、増分バックアップ以前のバックアップデータも必要です。
現在のデータを削除せずに過去のデータを参照するには、後述の `MOUNT` を使用します。


### 増分バックアップの注意事項 {#precautions-for-incremental-backup}

backup1 を基に backup2 を作成した場合、ディスク障害などで backup1 を失うと、backup2 から復元できません。

同様に、増分バックアップの連鎖の途中で以前のバックアップを失うと、それ以降のバックアップから復元できません。

次のように 3 回実行すると、backup3 の基になるのは backup2、backup2 の基になるのは backup1 です。

backup1 を失うと backup2 と backup3 の両方が使えなくなり、backup2 を失うと backup3 から復元できません。

```sql
Mach> BACKUP DATABASE INTO DISK = 'backup1'; /* フルバックアップを実行 */
Executed successfully.
Mach> ...
  
Mach> BACKUP DATABASE AFTER 'backup1' INTO DISK = 'backup2'; /* backup1 以降に入力したデータを増分バックアップ */
Executed successfully.
Mach> ...
 
Mach> BACKUP DATABASE AFTER 'backup2' INTO DISK = 'backup3'; /* backup2 以降に入力したデータを増分バックアップ */
Executed successfully.
Mach> ...
```


## データベースの復元 {#database-restore}

復元用の SQL 構文はありません。machadmin -r でオフライン復元します。実行前に次を確認してください。

* Machbase が停止していること。
* 既存のデータベースを削除していること。

```bash
machadmin -r backup_database_path;
```

```sql
backup database into disk = '/home/machbase/backup';
```

```bash
machadmin -k
machadmin -d
machadmin -r /home/machbase/backup;
```


## データベースのマウント {#database-mount}

障害に備えて定期的にバックアップしながらデータを追加し続けると、次の問題が発生します。

* データ保存用ディスクのコスト増加
* 稼働機器の物理ディスク容量の制限

現在のサービスに必要なデータだけを残して定期削除すると、この問題を軽減できます。ただし、過去のデータを参照するにはバックアップが必要です。大きなバックアップの復元には時間と追加の機器が必要で、既存データベースの削除も伴います。Machbase は、この問題を解決するマウント機能を提供します。

マウントは、稼働中のデータベースにバックアップを接続するオンライン機能です。複数のバックアップを接続し、1 つのデータベースのように参照できます。マウントしたデータベースは読み取り専用です。

`MOUNT` DATABASE は、バックアップしたデータベースやテーブルを、稼働中のデータベースから参照できる状態にします。通常と同じ DB コマンドで検索できます。

次の制約があります。

* バックアップとマウント先のデータベースで、DB とメタデータのメジャーバージョンに互換性が必要です。
* マウントしたデータは読み取り専用です。インデックスの作成、データの挿入と削除はできません。
* マウント済みデータベースの情報は、V$STORAGE_MOUNT_DATABASES で確認できます。
* 増分バックアップをマウントすると、そのバックアップに記録された差分だけを参照できます。以前のバックアップをたどって自動的にマウントすることはありません。


### マウント {#mount}

Backup_database_path にバックアップの保存場所、DatabaseName に他と区別できるマウント名を指定します。バックアップと同様に、相対パスは DB の設定にある DB_PATH を基準として解決されます。

```sql
MOUNT DATABASE 'backup_database_path' TO mount_name;
MOUNT DATABASE '/home/machbase/backup' TO mountdb;
```


### アンマウント {#unmount}

不要になったマウントは、アンマウントコマンドで解除できます。

```sql
UNMOUNT DATABASE mount_name;
UNMOUNT DATABASE mountdb;
```

### マウントした DB のデータ取得 {#mount-db-data-retrieval}

稼働中の DB と同じ SQL 文で、バックアップのデータを検索できます。

検索できるのは稼働中の DB の管理者 SYS だけです。テーブル名の前に MountDBName と UserName を付け、`.` で区切ります。MountDBName はマウントした DB、UserName はそのテーブルの所有者を示します。

```sql
SELECT column_name FROM mount_name.user_name.table_name;
```

```sql
SELECT * FROM mountdb.sys.backuptable;
```

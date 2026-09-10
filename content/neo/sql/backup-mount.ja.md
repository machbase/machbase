---
title: バックアップとマウント
type: docs
weight: 61
toc: true
---

## はじめに

産業現場のセンサーデータは、「産業用ビッグデータ」や「Smart-X」と呼ばれるほど急速に増加しています。大量の時系列データを継続的に保存するには、データのアーカイブ、災害復旧、過去データの分析を支える仕組みが必要です。従来のバックアップ・復元には、対象範囲を柔軟に設定しにくい、復元に時間がかかる、全体を復元するまでバックアップ内容を検索できないという制約があります。

Machbase は、時系列ワークロードに対応した **バックアップ（Backup）** と **マウント（Mount）** を提供します。全体、増分、時間範囲、テーブル単位のバックアップに対応し、マウントを使用すると、復元せずにバックアップを読み取り専用で接続して検索できます。

## 基本概念

* **Backup**: データベース全体、特定のテーブル、または時間範囲を外部ストレージに物理コピーします。データとメタデータのファイルを含むディレクトリとして保存します。
* **Restore**: バックアップからデータベースを復元します。災害復旧や複製環境の構築に使用します。`machbase-neo restore` は空の `dbs` ディレクトリを要求し、既存データがある場合は拒否します。
* **Mount**: バックアップディレクトリを、稼働中の Machbase インスタンスに読み取り専用データベースとして接続します。復元せずにバックアップ時点の固定されたデータを検索できます。
* **Unmount**: マウントしたバックアップを切り離します。バックアップファイル自体は削除しません。
* **Live Data**: 現在稼働している Machbase インスタンスのリアルタイムデータです。
* **Fossilized Data**: バックアップに含まれる特定時点または期間の不変データです。マウントすると読み取り専用でアクセスできます。

## バックアップ操作

要件に応じて、バックアップの範囲と種類を選択できます。

### 全体バックアップ（データベースまたはテーブル）

実行時点のデータベース全体、または指定したテーブルをコピーします。

```sql
BACKUP DATABASE INTO DISK = 'path/to/backup_directory_name';

BACKUP TABLE table_name INTO DISK = 'path/to/backup_directory_name';
```

- `DATABASE`: データベース全体をバックアップします。
- `TABLE table_name`: 指定したテーブルだけをバックアップします。
- `INTO DISK = 'パス'`: バックアップの出力先ディレクトリを指定します。絶対パス、または `$MACHBASE_HOME/dbs` を基準とする相対パスを使用できます。バックアップ処理が作成できる、新しい出力先パスを指定してください。

**補足**
- バックアップ開始時点のデータを取得します。
- 出力は、複数のファイルとサブディレクトリで構成されるディレクトリです。

### 増分バックアップ（データベースまたはテーブル）

前のバックアップ（通常は全体バックアップまたは直前の増分バックアップ）以降の変更データだけを取得します。後続のバックアップにかかる時間とストレージ容量を削減できます。

```sql
BACKUP DATABASE AFTER 'path/to/previous_backup' INTO DISK = 'path/to/incremental_backup_dir';

BACKUP TABLE table_name AFTER 'path/to/previous_backup' INTO DISK = 'path/to/incremental_backup_dir';
```

- `AFTER 'パス'`: バックアップチェーンの *直前* の全体または増分バックアップのディレクトリを指定します。存在し、アクセス可能である必要があります。
- `INTO DISK = 'パス'`: 新しい増分バックアップの出力先ディレクトリを指定します。

**補足**
- 主に LOG テーブルや TAG テーブルなど、追記が多いデータに適しています。
- LOOKUP テーブルは追記以外の変更もあるため、増分バックアップでも常に全体をバックアップします。
- 直前のバックアップディレクトリが完全な状態で存在する必要があります。

### 時間範囲バックアップ（データベースまたはテーブル）

指定した期間のデータをバックアップします。時系列データを月別や四半期別にアーカイブする場合に便利です。

```sql
BACKUP DATABASE
    FROM time_expression_start
    TO time_expression_end
    INTO DISK = 'path/to/backup_directory_name';

BACKUP TABLE table_name
    FROM time_expression_start
    TO time_expression_end
    INTO DISK = 'path/to/backup_directory_name';
```

- `FROM time_expression_start`: バックアップの開始時刻（含む）を指定します。例: `TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')`。
- `TO time_expression_end`: バックアップの終了時刻（含む）を指定します。

### ディスクバックアップのファイル構造

| パス・ファイル | 説明 |
|:--|:--|
| `<path>/backup.dat` | バックアップの状態・管理情報。Neo はこのファイルでバックアップを識別します。 |
| `<path>/backup.trc` | バックアップ処理のトレースファイル。 |
| その他の生成ファイル | データ、メタデータ、インデックスなど、復元・マウントに必要なファイル。バックアップディレクトリ全体を保持します。 |

## マウント操作

バックアップディレクトリを読み取り専用データベースとして接続します。復元せずに検索できます。

### バックアップのマウント

```sql
MOUNT DATABASE '/path/to/backup_directory' TO mount_name;
```

- `'/path/to/backup_directory'`: マウントするバックアップディレクトリのパス。
- `mount_name`: マウントの別名。データは `mount_name.スキーマ.テーブル` の形式で検索します。

異なる `mount_name` を指定すると、複数のバックアップを同時にマウントできます。

### マウントしたデータの検索

元のスキーマ所有者（通常は `sys`）とテーブル名をマウント名で修飾します。

```sql
SELECT column_list
FROM mount_name.user_name.table_name
WHERE [conditions];
```

- `mount_name`: マウント時に指定した別名。
- `user_name`: 元のテーブルのスキーマ所有者（通常は `sys`）。
- `table_name`: バックアップ内のテーブル名。

### マウントの例

```sql
MOUNT DATABASE '/backup/jan_data' TO backup_jan;

-- マウントしたデータを検索
SELECT COUNT(*) FROM backup_jan.sys.sensor_data;
SELECT * FROM backup_jan.sys.sensor_data
 WHERE time BETWEEN TO_DATE('2024-01-05') AND TO_DATE('2024-01-06');
```

### マウント解除

```sql
UNMOUNT DATABASE mount_name;
```

`mount_name` には切り離すマウントの別名を指定します。マウントを解除すると、そのバックアップデータを検索できなくなります。バックアップファイル自体は削除されません。

## 復元操作

`machbase-neo restore` は、停止したインスタンスのデータディレクトリにバックアップを復元します。対象のホームディレクトリは既存である必要があります。`dbs` がない場合は作成しますが、空でない場合はエラーになります。既存のデータを自動的に上書きする操作ではありません。

```bash
machbase-neo restore --data <machbase_home_dir> <path/to/backup_directory>
```

- `--data <machbase_home_dir>`: 復元先の `$MACHBASE_HOME` ディレクトリを指定します。
- `<path/to/backup_directory>`: 復元するバックアップディレクトリのパスです。
  - 全体バックアップを復元する場合は、そのディレクトリを指定します。
  - 増分バックアップを含めて復元する場合は、**最後の増分バックアップ**を指定します。先行するバックアップは自動的に検索して使用します。

**注意事項**
- 復元先のインスタンスを停止し、対象の `$MACHBASE_HOME` と既存データの保全を確認してください。`dbs` が空でない状態では復元できません。
- バックアップデータを書き換えるには復元が必要です。マウントは読み取り専用です。

## マウントの利点と注意事項

### 利点

- **迅速なアクセス**: 復元せずに過去のデータへアクセスでき、TB 単位のバックアップもすぐに確認できます。
- **インデックスの保持**: バックアップに含まれる時系列インデックスを使用して、マウントしたデータも高速に検索できます。
- **Rollup 構造の保持**: バックアップ時点の Rollup テーブルを保持し、稼働中のデータと同様に統計分析できます。
- **オンライン操作**: 稼働中のデータベースを停止せずにマウント・マウント解除を行えます。
- **リソースの節約**: 検索のためだけに全体復元のディスク I/O や CPU リソースを消費する必要がありません。

### 注意事項

- **読み取り専用**: マウントしたデータベースは読み取り専用です。`INSERT`、`UPDATE`、`DELETE`、DDL は実行できません。変更するには復元が必要です。
- **統計ビュー**: リアルタイム統計ビュー（`v$...`）は、マウントした静的データに適用できない場合があります。必要な情報は直接クエリで取得してください。
- **ファイルシステム権限**: Machbase サーバープロセスがバックアップディレクトリを読み取れる必要があります。

## 使用例

TAG テーブル `EQPT_A` と `EQPT_B` に、2024-01-01〜2024-06-30 のデータが格納されているものとします。

```sql
CREATE TAG TABLE IF NOT EXISTS EQPT_A (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) tag_partition_count=1;

CREATE TAG TABLE IF NOT EXISTS EQPT_B (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) tag_partition_count=1;

SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM EQPT_A;
SELECT COUNT(*) FROM EQPT_A;
```

### 例 1: データベース全体のバックアップとマウント

```sql
-- 1. 指定したディレクトリにデータベース全体をバックアップ
-- 新しい出力先パスを指定し、Machbase が作成できる権限を確認する
BACKUP DATABASE INTO DISK = '/backup/full_db_20240630'; -- 環境に合うパスを使用

-- 2. mount_fulldb という別名でバックアップをマウント
MOUNT DATABASE '/backup/full_db_20240630' TO mount_fulldb;

-- 3. マウントしたバックアップのデータを検索
-- マウントした EQPT_A の時間範囲を確認
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_fulldb.sys.EQPT_A;
-- マウントした EQPT_A の行数を確認
SELECT COUNT(*) FROM mount_fulldb.sys.EQPT_A;
-- マウントした EQPT_B のデータを検索
SELECT name, TO_CHAR(time), value FROM mount_fulldb.sys.EQPT_B LIMIT 5;

-- 4. アクセスが不要になったらマウントを解除
UNMOUNT DATABASE mount_fulldb;
```

### 例 2: 時間範囲を指定したデータベースのバックアップとマウント

```sql
-- 1. 2024 年 1 月 1 日から 3 月 31 日までのデータだけをバックアップ
BACKUP DATABASE
    FROM TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
    TO TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    INTO DISK = '/backup/db_2024Q1'; -- 環境に合うパスを使用

-- 2. 任意: 古いデータの削除をシミュレートする（稼働中のテーブルのデータを削除する操作）
DELETE FROM EQPT_A BEFORE TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
DELETE FROM EQPT_B BEFORE TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
-- 稼働中のテーブルのデータ件数が減ったことを確認
SELECT COUNT(*) FROM EQPT_A;

-- 3. 時間範囲を指定したバックアップをマウント
MOUNT DATABASE '/backup/db_2024Q1' TO mount_q1;

-- 4. マウントしたバックアップには元の第 1 四半期のデータが含まれる
SELECT COUNT(*) FROM mount_q1.sys.EQPT_A; -- 元の第 1 四半期の件数と一致する
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_q1.sys.EQPT_A; -- 第 1 四半期の時間範囲を示す

-- 稼働中のテーブル（削除後）とマウントしたテーブル（削除前）の件数を比較
SELECT COUNT(*) AS live_count FROM EQPT_A;
SELECT COUNT(*) AS mounted_q1_count FROM mount_q1.sys.EQPT_A;

-- 5. マウントを解除
UNMOUNT DATABASE mount_q1;
```

### 例 3: テーブルと時間範囲を指定したバックアップとマウント

```sql
-- 1. 2024 年 4 月 1 日から 5 月 15 日までの EQPT_A だけをバックアップ
BACKUP TABLE EQPT_A
    FROM TO_DATE('2024-04-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
    TO TO_DATE('2024-05-15 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    INTO DISK = '/backup/eqpta_20240401_20240515'; -- 環境に合うパスを使用

-- 2. テーブル単位のバックアップをマウント
MOUNT DATABASE '/backup/eqpta_20240401_20240515' TO mount_eqpta_partial;

-- 3. マウントしたバックアップを検索
-- 時間範囲と件数が指定したバックアップ範囲と一致することを確認
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_eqpta_partial.sys.EQPT_A;
SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_A;
-- 生データのサンプルを検索
SELECT name, TO_CHAR(time), value FROM mount_eqpta_partial.sys.EQPT_A LIMIT 5;

-- このマウントで EQPT_B を検索すると失敗する（バックアップに含まれないため）
-- SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_B; -- 想定されるエラー: テーブルが見つからない

-- 4. マウントを解除
UNMOUNT DATABASE mount_eqpta_partial;
```

### 例 4: 複数のバックアップの同時マウント

```sql
-- 前の例のバックアップが存在することを前提とする:
-- '/backup/db_2024Q1'（データベース全体、第 1 四半期）
-- '/backup/full_db_20240630'（データベース全体、6 月 30 日まで）
-- '/backup/eqpta_20240401_20240515'（EQPT_A のみ、4 月 1 日〜5 月 15 日）

-- 1. 異なる別名で 3 つのバックアップをマウント
MOUNT DATABASE '/backup/db_2024Q1' TO mount_q1;
MOUNT DATABASE '/backup/full_db_20240630' TO mount_jun30;
MOUNT DATABASE '/backup/eqpta_20240401_20240515' TO mount_eqpta_partial;

-- 2. 異なるマウントのデータを検索
-- 第 1 四半期のバックアップの EQPT_A の件数
SELECT COUNT(*) FROM mount_q1.sys.EQPT_A;
-- データベース全体のバックアップの EQPT_B の件数
SELECT COUNT(*) FROM mount_jun30.sys.EQPT_B;
-- テーブル単位の部分バックアップの EQPT_A の件数
SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_A;
-- 部分バックアップ内の EQPT_B を検索すると失敗する
-- SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_B;

-- 3. 完了したらすべてのマウントを解除
UNMOUNT DATABASE mount_q1;
UNMOUNT DATABASE mount_jun30;
UNMOUNT DATABASE mount_eqpta_partial;
```

バックアップとマウントを組み合わせると、稼働中のデータ量を抑えながら、過去のデータを検索・比較分析できます。必要に応じて全体を復元するか、マウントして過去のデータを読み取り専用で参照してください。
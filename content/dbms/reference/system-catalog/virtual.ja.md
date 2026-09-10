---
type: docs
title: '16.3.2 仮想テーブル辞典'
weight: 20
toc: true
---

仮想テーブル（動的ビュー）は`V$`で始まり、Machbaseサーバーの現在の運用状態をテーブル形式で表します。読み取り専用で、クエリのたびに最新の状態を返します。

## 仮想テーブル一覧

| カテゴリー | テーブル名 | 説明 |
|---------|------------|------|
| セッション/システム | `V$VERSION` | サーバーバージョン情報 |
| セッション/システム | `V$SESSION` | 現在の接続セッション一覧 |
| データベース | `V$DATABASES` | アクティブ/マウント済みデータベースの状態 |
| データベース | `V$DATABASE_OPERATIONS` | データベースのライフサイクル操作履歴 |
| セッション/システム | `V$STMT` | 実行中のSQL文 |
| セッション/システム | `V$PROPERTY` | 現在のサーバー設定値 |
| セッション/システム | `V$SYSMEM` | システムのメモリ使用量 |
| セッション/システム | `V$SYSSTAT` | システム統計情報 |
| セッション/システム | `V$SYSTIME` | システム時間統計 |
| ストレージ | `V$STORAGE` | ストレージファイルサイズの概要 |
| ストレージ | `V$STORAGE_USAGE` | ディスク使用量と使用率の上限 |
| ストレージ | `V$STORAGE_TABLES` | テーブル別のストレージ使用量 |
| ストレージ | `V$STORAGE_MOUNT_DATABASES` | マウント済みバックアップデータベース |
| タグRollup | `V$ROLLUP` | Rollupジョブの状態 |
| TAGテーブル | `V$<TABLE>_STAT` | テーブル別のタグ・軸統計。実際の名前はTAGテーブル名から生成 |
| ライセンス | `V$LICENSE_INFO` | ライセンス情報 |
| ロック | `V$MUTEX` | ロック状況 |

`V$<TABLE>_STAT`はTAGテーブルごとに動的に作成されるため、固定のグローバル仮想テーブル一覧とは
区別します。時間軸・距離軸別の列名と型は
[TAG別統計ビュー](/dbms/tag-table-usage/query-analysis/#tag-stat-axis-schema)を参照してください。

## V$VERSION

サーバーバージョン情報を参照します。

| 列名 | 説明 |
|----------|------|
| `BINARY_SIGNATURE` | サーバーバージョン文字列 |

```sql
SELECT binary_signature FROM v$version;
```

## V$DATABASES

論理データベースとマウント済みデータベースの状態を参照します。`DATABASE_ID`は論理カタログの
識別子であり、`TABLESPACE_ID`とは異なります。

| 列 | 説明 |
|------|------|
| `DATABASE_ID` | 論理データベース識別子 |
| `SOURCE_DATABASE_ID` | マウント済みバックアップの元のデータベース識別子 |
| `NAME` | データベース名またはマウントのエイリアス |
| `KIND` | `ACTIVE`または`MOUNTED` |
| `ACCESS_MODE` | `READ_WRITE`または`READ_ONLY` |
| `CAN_USE` | `USE`で選択できるかどうか |
| `STATE` | ライフサイクルの状態 |
| `IS_DEFAULT` | デフォルトの`MACHBASEDB`かどうか |

```sql
SELECT database_id, name, kind, access_mode, can_use, state, is_default
  FROM v$databases
 ORDER BY database_id;
```

## V$DATABASE_OPERATIONS

`CREATE`、`ALTER`、`DROP`、`BACKUP`、`RESTORE`、`MOUNT`、`UMOUNT`操作の状態とエラーを参照します。
`FAILED_NEEDS_ACTION`状態の場合は、実際の`V$DATABASES`の状態とサーバーログも確認してください。

| 列 | 説明 |
|------|------|
| `OPERATION_ID` | 操作識別子 |
| `DATABASE_ID` | 対象論理データベース識別子 |
| `DATABASE_NAME` | 対象データベース名 |
| `STATE` | 操作状態 |
| `LAST_ERROR` | 失敗原因 |
| `CREATED_AT` | 作成時刻 |
| `UPDATED_AT` | 最終変更時刻 |

```sql
SELECT operation_id, database_name, state, last_error
  FROM v$database_operations
 ORDER BY operation_id DESC;
```

## V$SESSION

現在の接続セッションの一覧と状態を表示します。

| 列名 | 説明 |
|----------|------|
| `ID` | セッション識別子 |
| `CLOSED` | 接続が閉じているかどうか（0: アクティブ） |
| `USER_ID` | ユーザー識別子 |
| `LOGIN_TIME` | 接続時刻 |
| `CLIENT_TYPE` | 接続クライアントのタイプ |
| `USER_NAME` | ユーザー名 |
| `USER_IP` | ユーザーIPアドレス |
| `SQL_LOGGING` | 該当セッションのトレースログ記録の有効化 |
| `IDLE_TIMEOUT` | アイドル状態のセッションを終了するまでの時間（秒） |
| `QUERY_TIMEOUT` | クエリ応答の待機時間 |

```sql
-- 現在のアクティブセッション一覧
SELECT id, user_name, user_ip, client_type, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time;
```

## V$STMT

現在実行中または待機中のSQL文の情報を表示します。

| 列名 | 説明 |
|----------|------|
| `ID` | クエリ識別子 |
| `SESS_ID` | クエリを実行したセッションの識別子 |
| `STATE` | クエリ状態 |
| `RECORD_SIZE` | SELECT実行時の結果レコードサイズ |
| `QUERY` | クエリのテキスト |

```sql
-- 実行中のクエリの確認
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';
```

## V$PROPERTY

サーバーに設定されたすべてのプロパティ値を参照します。

| 列名 | 説明 |
|----------|------|
| `NAME` | プロパティ名 |
| `VALUE` | 現在の設定値 |
| `TYPE` | データ型 |
| `DEFLT` | デフォルト値 |
| `MIN` | 最小値 |
| `MAX` | 最大値 |

```sql
-- 特定設定値の確認
SELECT name, value, deflt
  FROM v$property
 WHERE name IN ('PORT_NO', 'TRACE_LOG_LEVEL', 'MAX_SESSION_COUNT');

-- デフォルト値と異なる設定のみ参照
SELECT name, value, deflt
  FROM v$property
 WHERE value != deflt
 ORDER BY name;
```

## V$STORAGE_USAGE

ストレージシステムのディスク使用状況を表示します。

| 列名 | 説明 |
|----------|------|
| `TOTAL_SPACE` | データディレクトリがあるストレージの総容量 |
| `USED_SPACE` | 使用中の容量 |
| `USED_RATIO` | 使用率（%） |
| `RATIO_CAP` | 使用量の上限（超過時は取り込みを停止） |

```sql
SELECT total_space, used_space, used_ratio, ratio_cap
  FROM v$storage_usage;
```

## V$SYSMEM

システムのメモリ使用量を参照します。

| 列名 | 説明 |
|----------|------|
| `ID` | メモリマネージャー識別子 |
| `NAME` | メモリマネージャー名 |
| `USAGE` | 現在の使用量 |
| `MAX_USAGE` | 記録された最大使用量 |

```sql
SELECT name, usage, max_usage
  FROM v$sysmem
 ORDER BY usage DESC;
```

## V$LICENSE_INFO

サーバーのライセンス情報を参照します。

| 列名 | 説明 |
|----------|------|
| `ID` | ライセンスID |
| `ISSUE_DATE` | 発行日 |
| `TYPE` | ライセンスタイプ |
| `CUSTOMER` | 顧客名 |
| `PROJECT` | プロジェクト名 |
| `INSTALL_DATE` | インストール日 |
| `VIOLATE_STATUS` | ライセンス違反状態 |
| `VIOLATE_MSG` | ライセンス違反メッセージ |

```sql
SELECT id, type, customer, issue_date,
       install_date, violate_status, violate_msg
  FROM v$license_info;
```

## 全仮想テーブル一覧の確認

```sql
-- 現在のサーバーで参照できる全V$仮想テーブル一覧
SELECT name
  FROM v$tables
 WHERE name LIKE 'V$%'
 ORDER BY name;
```

> 仮想テーブルは読み取り専用です。Cluster Editionでのみ提供するテーブル（V$NODE_STATUS、V$REPLICATIONなど）は、Standard Editionでは参照できません。

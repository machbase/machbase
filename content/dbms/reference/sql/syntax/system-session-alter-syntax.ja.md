---
type: docs
title: 'SYSTEM/SESSION/ALTER SYSTEM'
weight: 210
toc: true
---

`ALTER SYSTEM`はサーバー全体のリソースを管理する構文です。`ALTER SESSION`は現在のセッションだけに適用するパラメーターを設定します。

> **権限**: `ALTER SYSTEM`は`SYS`アカウント、または`GRANT ALTER ON DATABASE database_name TO user_name;`で権限を付与されたユーザーのみ実行できます。

---

## ALTER SYSTEM {#alter-system}

### コマンド一覧

| コマンド | 説明 |
|--------|------|
| `KILL SESSION n` | 指定セッションを強制終了 |
| `CANCEL SESSION n` | セッションを維持し、実行中のクエリだけをキャンセル |
| `CHECKPOINT` | メモリバッファーを直ちにディスクへ同期 |
| `FREEZE` | 全DMLを一時停止（バックアップ準備用） |
| `UNFREEZE` | FREEZEで停止したDMLを再開 |
| `FLUSH AGER` | Agerスレッドを直ちに実行して期限切れデータを整理 |
| `FLUSH SYS_STAT` | クエリオプティマイザー用のシステム統計を更新 |
| `FLUSH PVO_CACHE` | PVO Statementキャッシュを初期化 |
| `FLUSH PAGE_CACHE` | OSページキャッシュを強制解放 |
| `FLUSH TAG_CACHE` | TAGテーブルのメタデータキャッシュを初期化 |
| `INSTALL LICENSE` | デフォルトパスのライセンスファイルをインストール |
| `INSTALL LICENSE = 'path'` | 指定パスのライセンスファイルをインストール |
| `CHECK DISK_USAGE` | LOGテーブルのディスク使用量を再計算 |
| `SET property = value` | システムプロパティの動的変更 |

---

### KILL SESSION / CANCEL SESSION

```sql
alter_system_kill_session_stmt   ::= 'ALTER SYSTEM KILL SESSION'   session_id
alter_system_cancel_session_stmt ::= 'ALTER SYSTEM CANCEL SESSION' session_id
```

```sql
-- 現在のセッション一覧を確認
SELECT id, user_id, client_type FROM v$session;

-- セッションを強制終了（切断、トランザクションをロールバック）
ALTER SYSTEM KILL SESSION 12;

-- 実行中のクエリだけをキャンセル（接続を維持）
ALTER SYSTEM CANCEL SESSION 6;
```

- `KILL SESSION`: SYSユーザーのみ実行可能。対象セッションを即座に終了します。
- `CANCEL SESSION`: 同じユーザーまたはSYSのみ実行可能。セッションを維持し、現在実行中のSQLだけを中止します。

---

### CHECKPOINT

```sql
alter_system_checkpoint_stmt ::= 'ALTER SYSTEM CHECKPOINT'
```

メモリにバッファーされたデータを直ちにディスクへ同期します。

```sql
ALTER SYSTEM CHECKPOINT;
```

---

### FREEZE / UNFREEZE

```sql
alter_system_freeze_stmt   ::= 'ALTER SYSTEM FREEZE'
alter_system_unfreeze_stmt ::= 'ALTER SYSTEM UNFREEZE'
```

バックアップ準備など整合性が必要な場合、すべてのDMLを一時停止します。

```sql
ALTER SYSTEM FREEZE;
-- (バックアップまたは点検を実行)
ALTER SYSTEM UNFREEZE;
```

---

### FLUSH

```sql
alter_system_flush_stmt ::=
    'ALTER SYSTEM FLUSH'
    ( 'AGER'
    | 'SYS_STAT'
    | 'PVO_CACHE'
    | 'PAGE_CACHE'
    | 'TAG_CACHE' )
```

```sql
-- Agerを即時実行（期限切れデータを整理）
ALTER SYSTEM FLUSH AGER;

-- クエリオプティマイザーの統計を更新
ALTER SYSTEM FLUSH SYS_STAT;

-- PVO Statementキャッシュを初期化
ALTER SYSTEM FLUSH PVO_CACHE;

-- OSページキャッシュを強制解放
ALTER SYSTEM FLUSH PAGE_CACHE;

-- TAGメタデータキャッシュを初期化
ALTER SYSTEM FLUSH TAG_CACHE;
```

---

### INSTALL LICENSE

```sql
-- デフォルトパス ($MACHBASE_HOME/conf/license.dat)
alter_system_install_license_stmt ::= 'ALTER SYSTEM INSTALL LICENSE'

-- 指定パス
alter_system_install_license_path_stmt ::= 'ALTER SYSTEM INSTALL LICENSE' '=' "'" path "'"
```

```sql
-- デフォルトパスからインストール
ALTER SYSTEM INSTALL LICENSE;

-- 指定パスからインストール
ALTER SYSTEM INSTALL LICENSE = '/tmp/new_license.dat';
```

---

### CHECK DISK_USAGE

```sql
alter_system_check_disk_stmt ::= 'ALTER SYSTEM CHECK DISK_USAGE'
```

`V$STORAGE`の`DC_TABLE_FILE_SIZE`値をファイルシステムから再計算します。プロセス障害や停電後に使用量が不正確な場合に使用します。

```sql
ALTER SYSTEM CHECK DISK_USAGE;
```

---

### SET (システムプロパティの動的変更)

```sql
alter_system_set_stmt ::=
    'ALTER SYSTEM SET' property_name '=' value_expr

value_expr ::=
    value
  | property_name '|'  number   -- ビットOR（フラグ追加）
  | property_name '&' '~' number -- ビットAND NOT（フラグ削除）
```

変更できるプロパティ一覧:

| プロパティ | 説明 |
|------|------|
| `QUERY_PARALLEL_FACTOR` | クエリの並列処理スレッド数 |
| `DEFAULT_DATE_FORMAT` | デフォルトの日付形式（例: `'YYYY-MM-DD HH24:MI:SS'`） |
| `TRACE_LOG_LEVEL` | トレースログレベル（ビットフラグ） |
| `DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE` | ディスク列指向ページキャッシュの最大サイズ |
| `MAX_SESSION_COUNT` | 最大セッション数 |
| `SESSION_IDLE_TIMEOUT_SEC` | セッションのアイドルタイムアウト（秒） |
| `PROCESS_MAX_SIZE` | プロセスの最大メモリサイズ |
| `TAG_CACHE_MAX_MEMORY_SIZE` | TAGキャッシュの最大メモリサイズ |
| `PVO_CACHE_ENABLE` | PVOキャッシュの有効化（0/1） |
| `PVO_CACHE_MAX_MEMORY_SIZE` | PVOキャッシュの最大メモリサイズ |

```sql
-- 値を直接設定
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET DEFAULT_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';
-- 変更前の現在値を確認
SELECT NAME, VALUE, MIN, MAX
  FROM V$PROPERTY
 WHERE NAME = 'MAX_SESSION_COUNT';

-- ビットフラグの追加（OR）
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL | 0x00000004;

-- ビットフラグの削除（AND NOT）
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL & ~0x00000001;

-- 16進数で設定
ALTER SYSTEM SET TRACE_LOG_LEVEL = 0x00000003;
```

---

## ALTER SESSION {#alter-session}

セッション単位のパラメーターを変更します。

```sql
alter_session_stmt ::=
    'ALTER SESSION SET' session_property_name '=' value
```

### SET SQL_LOGGING

```sql
ALTER SESSION SET SQL_LOGGING = flag
-- flag: ビットORの組み合わせ
-- 0x1: 解析・検証・最適化段階のログ
-- 0x2: DDL実行結果のログ
```

```sql
ALTER SESSION SET SQL_LOGGING = 3;  -- 解析ログ + DDLログ
ALTER SESSION SET SQL_LOGGING = 0;  -- ログ記録を無効化
```

### SET DEFAULT_DATE_FORMAT

```sql
ALTER SESSION SET DEFAULT_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';
ALTER SESSION SET DEFAULT_DATE_FORMAT = 'YYYYMMDD';
```

### SET SHOW_HIDDEN_COLS

`SELECT *`で隠し列（`_arrival_time`）も表示するか設定します。

```sql
ALTER SESSION SET SHOW_HIDDEN_COLS = 1;  -- 隠し列を表示
ALTER SESSION SET SHOW_HIDDEN_COLS = 0;  -- 隠し列を非表示（デフォルト）
```

### SET FEEDBACK_APPEND_ERROR

Append APIのエラーメッセージをクライアントへ送信するか設定します。

```sql
ALTER SESSION SET FEEDBACK_APPEND_ERROR = 1;  -- エラーメッセージを送信（サーバーのデフォルト）
ALTER SESSION SET FEEDBACK_APPEND_ERROR = 0;  -- エラーメッセージを送信しない
```

### SET MAX_QPX_MEM

単一SQLのGROUP BY、DISTINCT、ORDER BYで使用できる最大メモリ（バイト）です。

```sql
ALTER SESSION SET MAX_QPX_MEM = 1073741824;  -- 1GB
```

### SET DDL_LOCK_TIMEOUT

Standard Editionで競合するDDLロックの待機時間を秒単位で指定します。デフォルトは`0`、範囲は`0`~`1000000`です。
`0`の場合は待機せず、直ちに`ERR-02031: Resource busy (<object>)`を返します。

```sql
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;  -- 最大10秒待機
```

実行中のDDLの待機時間は変わらず、新しい値は次のDDLから適用します。セッションごとの現在値は
`V$SESSION.DDL_LOCK_TIMEOUT`で確認します。

```sql
SELECT id, user_name, ddl_lock_timeout
  FROM v$session
 WHERE closed = 0
 ORDER BY id;
```

競合範囲とエラー処理は[DDLの同時実行とロック](../ddl-syntax/#ddl-concurrency)を参照してください。

### SET SESSION_IDLE_TIMEOUT_SEC

アイドル状態のセッションで接続を維持する最大時間（秒）です。

```sql
ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC = 300;  -- 5分
```

### SET QUERY_TIMEOUT

クエリ実行の最大待機時間（秒）です。超過するとクエリを自動中止します。

```sql
ALTER SESSION SET QUERY_TIMEOUT = 60;  -- 60秒
```

---

## 関連ビュー

| ビュー | 説明 |
|----|------|
| `v$session` | 現在の接続セッション一覧とセッション別パラメーター |
| `v$storage` | ディスク使用量情報（`DC_TABLE_FILE_SIZE`など） |
| `v$license_info` | インストール済みライセンス情報 |
| `v$property` | システムプロパティと現在値 |

```sql
-- セッション一覧を参照
SELECT id, user_id, client_type, login_time FROM v$session;

-- システムプロパティを確認
SELECT name, value FROM v$property WHERE name = 'TRACE_LOG_LEVEL';
```

---

## 関連ドキュメント

- [ALTER SYSTEM運用ガイド](../../../../operations-configuration-recovery/alter-system/) - 詳細な運用手順とコマンド別の動作説明
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) - ALTER SYSTEM権限の付与

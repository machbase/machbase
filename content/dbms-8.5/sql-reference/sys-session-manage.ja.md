---
title : 'システムとセッションの管理'
type: docs
weight: 80
toc: true
---

# 目次 {#index}

* [ALTER SYSTEM](#alter-system)
    * [KILL SESSION](#kill-session)
    * [CANCEL SESSION](#cancel-session)
    * [CHECK DISK_USAGE](#check-disk_usage)
    * [INSTALL LICENSE](#install-license)
    * [INSTALL LICENSE (PATH)](#install-license-path)
    * [SET](#set)
    * [SET PVO CACHE](#set-pvo-cache)
    * [FLUSH PVO_CACHE](#flush-pvo_cache)
* [ALTER SESSION](#alter-session)
    * [SET SQL_LOGGING](#set-sql_logging)
    * [SET DEFAULT_DATE_FORMAT](#set-default_date_format)
    * [SET SHOW_HIDDEN_COLS](#set-show_hidden_cols)
    * [SET FEEDBACK_APPEND_ERROR](#set-feedback_append_error)
    * [SET MAX_QPX_MEM](#set-max_qpx_mem)
    * [SET SESSION_IDLE_TIMEOUT_SEC](#set-session_idle_timeout_sec)
    * [SET QUERY_TIMEOUT](#set-query_timeout)


## `ALTER SYSTEM` {#alter-system}

システム全体のリソース管理や設定変更を行う構文です。

> **注意**：8.5 以降で一般ユーザーが `ALTER SYSTEM` を実行するには、`MACHBASEDB` の `ALTER` 権限が必要です。[ユーザー管理](../user-manage/#grantrevoke)の `GRANT/REVOKE` を参照してください。例えば `GRANT ALTER ON machbasedb TO user_name;` で付与します。

### KILL SESSION {#kill-session}

**alter_system_kill_session_stmt:**

![alter_system_kill_session_stmt](/images/sql/sys/alter_system_kill_session_stmt.png)

```sql
alter_system_kill_session_stmt: 'ALTER SYSTEM KILL SESSION' number
```

SessionID で指定したセッションを終了します。

- `SYS` だけが実行できます。自身の終了、または `SYS` 以外からの実行は `[ERR-03025: Not enough privileges to manipulate the session. (<sid>)]` になります。
- 対象がなければ `ERR_MM_SESSION_ID_NOT_FOUND` を返します。
- 接続全体を終了する場合に使用します。対象セッションは切断されます。各文の自動コミットで確定済みのデータを巻き戻す機能ではありません。

例
```sql
-- SYS として実行
SELECT id, user_id, client_type FROM v$session;
ALTER SYSTEM KILL SESSION 12;
```

### CANCEL SESSION {#cancel-session}

**alter_system_cancel_session_stmt:**

![alter_system_cancel_session_stmt](/images/sql/sys/alter_system_cancel_session_stmt.png)

```sql
alter_system_cancel_session_stmt ::= 'ALTER SYSTEM CANCEL SESSION' number
```

SessionID で指定したセッションの処理を取り消します。

- 実行中の文だけを取り消し、接続は維持します。対象には `[ERR-03027: This statement has been canceled.]` が返ります。
- 同じユーザーまたは `SYS` が実行できます。別ユーザーには `[ERR-03026: You should log in with the same user name in the target session. Now (<me>) Target(<them>)]` を返します。
- 自身の取り消しは `[ERR-03025: Not enough privileges to manipulate the session. (<sid>)]` になります。
- 対象 ID がなければ `ERR_MM_SESSION_ID_NOT_FOUND` を返します。

例
```sql
-- セッション A：対象 SID を確認
SELECT id, user_id, client_type FROM v$session;

-- セッション B（同じユーザーまたは SYS）：SID 6 の実行を取り消す
ALTER SYSTEM CANCEL SESSION 6;
```

### CHECK DISK_USAGE {#check-disk_usage}

**alter_system_check_disk_stmt:**

![alter_system_check_disk_stmt](/images/sql/sys/alter_system_check_disk_stmt.png)

```sql
alter_system_check_disk_stmt ::= 'ALTER SYSTEM CHECK DISK_USAGE'
```

V$STORAGE の Log テーブル使用量 DC_TABLE_FILE_SIZE を補正します。

プロセス障害や停電後に不正確な場合、ファイルシステムから正しい値を読み取ります。ただし、負荷が大きいため頻繁な実行は避けてください。

### INSTALL LICENSE {#install-license}

**alter_system_install_license_stmt:**

![alter_system_install_license_stmt](/images/sql/sys/alter_system_install_license_stmt.png)

```sql
alter_system_install_license_stmt ::= 'ALTER SYSTEM INSTALL LICENSE'
```

既定の場所 $MACHBASE_HOME/conf/license.dat のライセンスを導入します。

適切なライセンスであるかを確認してから適用します。

### INSTALL LICENSE (PATH) {#install-license-path}

**alter_system_install_license_path_stmt:**

![alter_system_install_license_path_stmt](/images/sql/sys/alter_system_install_license_path_stmt.png)

```sql
alter_system_install_license_path_stmt: ::= 'ALTER SYSTEM INSTALL LICENSE' '=' "'" path "'"
```

指定した場所のライセンスを導入します。

ファイルが存在しない場合や不正な場合はエラーになります。絶対パスを指定してください。有効性を確認して適用します。

### SET {#set}

**alter_system_set_stmt:**

![alter_system_set_stmt](/images/sql/sys/alter_system_set_stmt.png)

```sql
alter_system_set_stmt ::= 'ALTER SYSTEM SET' prop_name '=' value
```

変更可能なプロパティは次のとおりです。
* QUERY_PARALLEL_FACTOR
* DEFAULT_DATE_FORMAT
* TRACE_LOG_LEVEL
* DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE
* MAX_SESSION_COUNT
* SESSION_IDLE_TIMEOUT_SEC
* PROCESS_MAX_SIZE
* TAG_CACHE_MAX_MEMORY_SIZE

数値プロパティには、拡張式を使用できます。

対応構文
- 直接代入（数値または文字列）：
  - `ALTER SYSTEM SET <name> = <value>;`
- フラグの追加（ビット OR）：
  - `ALTER SYSTEM SET <name> = <name> | <number>;`
  - `ALTER SYSTEM SET <name> = <number> | <name>;`
- フラグの解除（ビット AND と NOT）：
  - `ALTER SYSTEM SET <name> = <name> & ~<number>;`
  - `ALTER SYSTEM SET <name> = ~<number> & <name>;`

リテラルの規則
- `<number>` は 10 進数（`123`）または 16 進数（`0x7B`、`0X7B`）。
- ビット式は数値プロパティだけに使用でき、それ以外はエラーになります。
- `0xABCD` を文字列として指定するには、引用符を付けます。
  - `ALTER SYSTEM SET <name> = '0xABCD';`

注意事項
- 式内のプロパティ名は、左辺と一致する必要があります。
- 式を使わない既存の動作は変わりません。

例
```sql
-- TRACE_LOG_LEVEL を 16 進数で設定
ALTER SYSTEM SET TRACE_LOG_LEVEL=0x00000003;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- フラグを追加（ビット OR）
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL | 0x00000004;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = 0x00000008 | TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = 16 | TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- フラグを解除（ビット AND と NOT）
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL & ~0x00000001;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = ~0x00000002 & TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = ~4 & TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- 非数値のプロパティにはビット式を使用できない（エラー）
ALTER SYSTEM SET TRACE_LOG_LEVEL = 1 | DEFAULT_DATE_FORMAT;
ALTER SYSTEM SET DEFAULT_DATE_FORMAT = DEFAULT_DATE_FORMAT | 1;

-- 10 進数の代入
ALTER SYSTEM SET TRACE_LOG_LEVEL=277;
```

### SET PVO CACHE {#set-pvo-cache}

グローバル PVO ステートメントキャッシュを実行中に調整します（Standard のみ）。`PVO_CACHE_ENABLE`、`PVO_CACHE_MAX_MEMORY_SIZE`、`PVO_CACHE_MAX_PLANS_PER_SQL`、`PVO_CACHE_MAX_SQL_ENTRIES` は即時反映されます。`PVO_CACHE_SHARD_COUNT` は起動時初期化なので再起動が必要です。メモリと項目数の上限はシャードに分配されます。

```sql
ALTER SYSTEM SET PVO_CACHE_ENABLE = 1;
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 268435456;
ALTER SYSTEM SET PVO_CACHE_MAX_PLANS_PER_SQL = 512;
ALTER SYSTEM SET PVO_CACHE_MAX_SQL_ENTRIES = 0;
```

### FLUSH PVO_CACHE {#flush-pvo_cache}

PVO キャッシュだけを消去します。`FLUSH RESULT_CACHE` とは独立しています。DDL 成功時にも、内部で PVO キャッシュを消去します。

```sql
ALTER SYSTEM FLUSH PVO_CACHE;
```


## `ALTER` SESSION {#alter-session}

セッション単位のリソース管理や設定変更を行う構文です。

### SET SQL_LOGGING {#set-sql_logging}

**alter_session_sql_logging_stmt:**

![alter_session_sql_logging_stmt](/images/sql/sys/alter_session_sql_logging_stmt.png)

```sql
alter_session_sql_logging_stmt ::= 'ALTER SESSION SET SQL_LOGGING' '=' flag
```

セッションのトレースログ出力を設定します。

次のビットフラグを使用します。
* 0x1：解析、検証、最適化。
* 0x2：DDL の実行結果。

2 は DDL のみ、3 はエラーと DDL の両方を記録します。
ログフラグを変更してエラーを記録する例です。

```sql
Mach> alter session set SQL_LOGGING=1;
Altered successfully.
Mach> exit
```

### SET DEFAULT_DATE_FORMAT {#set-default_date_format}

**alter_session_set_defalut_dateformat_stmt:**

![alter_session_set_defalut_dateformat_stmt](/images/sql/sys/alter_session_set_defalut_dateformat_stmt.png)

```sql
alter_session_set_defalut_dateformat_stmt ::= 'ALTER SESSION SET DEFAULT_DATE_FORMAT' '=' date_format
```
セッションの DATETIME の既定書式を設定します。

サーバー起動時の DEFAULT_DATE_FORMAT がセッション属性に設定されます。
未変更の場合は YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn です。
システム全体とは別に、特定セッションの既定書式を変更できます。
V$SESSION で各セッションの書式を確認できます。確認と変更の例を示します。

```sql
Mach> CREATE TABLE time_table (time datetime);
Created successfully.
 
Mach> SELECT DEFAULT_DATE_FORMAT from v$session;
default_date_format                                                              
-----------------------------------------------
YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                
[1] row(s) selected.
 
Mach> INSERT INTO time_table VALUES(TO_DATE('2016/11/12'));
[ERR-00300: Invalid date value.(2016/11/12)]
 
Mach> ALTER SESSION SET DEFAULT_DATE_FORMAT='YYYY/MM/DD';
Altered successfully.
 
Mach> SELECT DEFAULT_DATE_FORMAT from v$session;
 
default_date_format                                                              
----------------------------------------------
YYYY/MM/DD                                                                       
[1] row(s) selected.
 
Mach> INSERT INTO time_table VALUES(TO_DATE('2016/11/12'));
1 row(s) inserted.
 
Mach> SELECT * FROM time_table;
 
TIME                              
----------------------------------
2016/11/12
 
[1] row(s) selected.
```

### SET SHOW_HIDDEN_COLS {#set-show_hidden_cols}

**alter_session_set_hidden_column_stmt:**

![alter_session_set_hidden_column_stmt](/images/sql/sys/alter_session_set_hidden_column_stmt.png)

```sql
alter_session_set_hidden_column_stmt ::= 'ALTER SESSION SET SHOW_HIDDEN_COLS' '=' ( '0' | '1' )
```

SELECT * の結果に隠し列 _arrival_time を含めるかを設定します。

起動時のグローバル SHOW_HIDDEN_COLS は 0 で、セッションに引き継がれます。
表示するには 1 に変更します。
V$SESSION で各セッションの SHOW_HIDDEN_COLS を確認できます。


```sql
Mach> SELECT * FROM  v$session;
ID                   CLOSED      USER_ID     LOGIN_TIME                      SQL_LOGGING SHOW_HIDDEN_COLS
-----------------------------------------------------------------------------------------------------------------
DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE
------------------------------------------------------------------------------------------------------
1                    0           1           2015-04-29 17:23:56 248:263:000 3           0
YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011
[1] row(s) selected.                            
Mach> ALTER SESSION SET SHOW_HIDDEN_COLS=1;
Altered successfully.
Mach> SELECT * FROM v$session;
_ARRIVAL_TIME                   ID                   CLOSED      USER_ID     LOGIN_TIME                      SQL_LOGGING
--------------------------------------------------------------------------------------------------------------------------------
SHOW_HIDDEN_COLS DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE
------------------------------------------------------------------------------------------------------------------------
1970-01-01 09:00:00 000:000:000 1                    0           1           2015-04-29 17:23:56 248:263:000 3
1           YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011
[1] row(s) selected.
```

### SET FEEDBACK_APPEND_ERROR {#set-feedback_append_error}

**alter_session_set_feedback_append_err_stmt:**

![alter_session_set_feedback_append_err_stmt](/images/sql/sys/alter_session_set_feedback_append_err_stmt.png)

```sql
alter_session_set_feedback_append_err_stmt ::= 'ALTER SESSION SET FEEDBACK_APPEND_ERROR' '=' ( '0' | '1' )
```

APPEND のエラーをクライアントへ送信するかを設定します。

指定値：
* 0：送信しない。
* 1：送信する。
使用例を示します。

```sql
mach> ALTER SESSION SET FEEDBACK_APPEND_ERROR=0;
Altered successfully.
```

### SET MAX_QPX_MEM {#set-max_qpx_mem}

**alter_session_set_max_qpx_mem_stmt:**

![alter_session_set_max_qpx_mem_stmt](/images/sql/sys/alter_session_set_max_qpx_mem_stmt.png)

```sql
alter_session_set_max_qpx_mem_stmt ::= 'ALTER SESSION SET MAX_QPX_MEM' '=' value
```

1 つの SQL が GROUP BY、DISTINCT、ORDER BY で使用する最大メモリ量を指定します。

上限を超えて確保しようとすると、その SQL を中止してエラーにします。
クエリーとともに、エラーコードとメッセージを machbase.trc に記録します。

```sql
Mach> ALTER SESSION SET MAX_QPX_MEM=1073741824;
Altered successfully.
 
Mach> SELECT * FROM v$session;
ID                   CLOSED      USER_ID     LOGIN_TIME                      CLIENT_TYPE                                                                      
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
USER_NAME                                                                         USER_IP                                                                           SQL_LOGGING SHOW_HIDDEN_COLS
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FEEDBACK_APPEND_ERROR DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE MAX_QPX_MEM          RS_CACHE_ENABLE      RS_CACHE_TIME_BOUND_MSEC
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
RS_CACHE_MAX_MEMORY_PER_QUERY RS_CACHE_MAX_RECORD_PER_QUERY RS_CACHE_APPROXIMATE_RESULT_ENABLE IDLE_TIMEOUT         QUERY_TIMEOUT       
-----------------------------------------------------------------------------------------------------------------------------------------------
14                   0           1           2021-03-08 16:33:01 503:181:809 CLI                                                                              
NULL                                                                              192.168.0.194                                                                     11          0               
1                     YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011            1073741824           1                    1000                    
16777216                      50000                         0                                  0                    0                   
[1] row(s) selected.
Elapsed time: 0.001
```

- SQL が最大メモリ量を超えた場合の trc エラー

```sql
[2021-03-08 16:36:32 P-69000 T-140515328653056][INFO] DML FAILURE (2E10000084:Memory allocation error (alloc'd: 1048595, max: 1048576).)
```

- 同じ場合の machsql エラー

```sql
Mach> select * from tag order by value DESC, time ASC;
NAME                  TIME                            VALUE                      
--------------------------------------------------------------------------------------
[ERR-00132: Memory allocation error (alloc'd: 1048595, max: 1048576).]
[0] row(s) selected.
Elapsed time: 0.447
```

### SET SESSION_IDLE_TIMEOUT_SEC {#set-session_idle_timeout_sec}

**alter_session_set_session_idle_timeout_sec_stmt:**

![alter_session_set_session_idle_timeout_sec_stmt](/images/sql/sys/alter_session_set_session_idle_timeout_sec_stmt.png)

```sql
alter_session_set_session_idle_timeout_sec_stmt ::= 'ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC' '=' value
```

アイドル状態で接続を維持する時間を指定します。
単位は秒です。設定時間が経過するとセッションを終了します。
V$SESSION で設定値を確認できます。

```sql
Mach> ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC=200;
Altered successfully.
 
 
Mach> SELECT IDLE_TIMEOUT FROM V$SESSION;
IDLE_TIMEOUT        
-----------------------
200                                     
[1] row(s) selected.
```

### SET QUERY_TIMEOUT {#set-query_timeout}

**alter_session_set_query_timeout_stmt:**

![alter_session_set_query_timeout_stmt](/images/sql/sys/alter_session_set_query_timeout_stmt.png)

```sql
alter_session_set_query_timeout_stmt ::= 'ALTER SESSION SET QUERY_TIMEOUT' '=' value
```

セッションのクエリー実行時に、サーバー応答を待つ時間です。
単位は秒です。実行後に指定時間を超えるとクエリーを終了します。
V$SESSION でセッションの QUERY_TIMEOUT を確認できます。

```sql
Mach> ALTER SESSION SET QUERY_TIMEOUT=200;
Altered successfully.
 
Mach> SELECT QUERY_TIMEOUT FROM V$SESSION;
QUERY_TIMEOUT        
-----------------------
200                                     
[1] row(s) selected.
```
